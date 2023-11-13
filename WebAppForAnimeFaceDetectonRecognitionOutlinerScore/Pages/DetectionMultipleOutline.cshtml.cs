using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.ComponentModel.DataAnnotations;
using System.IO.Compression;
using System.Net.Http.Headers;

namespace PPP_PAI_OiRPOS.Pages
{
    public class DetectionMultipleOutlineModel : PageModel
    {
        private readonly ILogger<DetectionMultipleOutlineModel> _logger;

        public string ErrorMessage { get; set; }
        public List<(string, string)> Images { get; set; }

        [BindProperty]
        public List<IFormFile> Files { get; set; }

        [BindProperty]
        public string Model { get; set; }

        [BindProperty]
        [Range(0, 1)]
        public float Threshold { get; set; } = 0.7f;

        public DetectionMultipleOutlineModel(ILogger<DetectionMultipleOutlineModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }

        public async Task<IActionResult> OnPost()
        {
            string model = Model;
            float threshold = Threshold;
            List<IFormFile> files = Files;
            ErrorMessage = "";
            Images = new List<(string, string)>();

            _logger.LogInformation($"Detection multiple OnPost() - {Images}");
            if (files.Count == 0)
            {
                ErrorMessage = "No Files sended";
                return Page();
            }

            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri("http://localhost:8000");
                var form = new MultipartFormDataContent();
                form.Add(new StringContent(model), "model");
                form.Add(new StringContent(threshold.ToString().Replace(',', '.')), "threshold");

                var streams = ConvertIFormFilesToStreams(files);
                foreach (var stream in streams)
                {
                    form.Add(CreateFileContent(stream.Stream, stream.FileName, stream.ContentType), "files");
                }

                _logger.LogInformation("Sending Post Async to Flask");
                var response = await client.PostAsync("/detectFaceOutliners", form);
                _logger.LogInformation("Revcivig result form Async to Flask");

                if (!response.IsSuccessStatusCode)
                {
                    ErrorMessage = response.StatusCode.ToString();
                    return Page();
                }

                // Read the response content as a stream
                using (var responseStream = await response.Content.ReadAsStreamAsync())
                {
                    try
                    {
                        using (var archive = new ZipArchive(responseStream, ZipArchiveMode.Read))
                        {
                            foreach (ZipArchiveEntry entry in archive.Entries)
                            {
                                if (entry.FullName.Contains(".png"))
                                {
                                    // Extract each entry (file) to a specific directory or do other processing as needed
                                    using (Stream entryStream = entry.Open())
                                    {
                                        using (MemoryStream memoryStream = new MemoryStream())
                                        {
                                            entryStream.CopyTo(memoryStream);
                                            byte[] bytes = memoryStream.ToArray();
                                            string base64String = Convert.ToBase64String(bytes);
                                            Images.Add(($"data:image/jpeg;base64,{base64String}", entry.FullName));
                                        }
                                    }
                                }
                            }
                            foreach (ZipArchiveEntry entry in archive.Entries)
                            {
                                if (entry.FullName.Contains(".txt"))
                                {
                                    using (StreamReader reader = new StreamReader(entry.Open()))
                                    {
                                        while (!reader.EndOfStream)
                                        {
                                            string line = reader.ReadLine();
                                            if (line == null) continue;

                                            // Assuming the score is separated by a space, adjust accordingly
                                            string[] parts = line.Split(' ');

                                            // Assuming the format of Images is (image, fileName)
                                            var imageEntry = Images.FirstOrDefault(img => img.Item2 == parts[1]);

                                            if (imageEntry != default)
                                            {
                                                // Add "score: " + the first part of the line to the existing tuple
                                                Images[Images.IndexOf(imageEntry)] = (imageEntry.Item1, imageEntry.Item2 + $" score: {parts[0]}");
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    catch (InvalidDataException ex)
                    {
                        // Handle the exception (e.g., log it or take appropriate action)
                        // This is where you can deal with the case where the response is not a valid ZIP file.
                        ErrorMessage = ex.Message;
                        return Page();
                    }
                }

            }
            return Page();
        }

        private StreamContent CreateFileContent(Stream stream, string fileName, string contentType)
        {
            var fileContent = new StreamContent(stream);
            fileContent.Headers.ContentDisposition = new ContentDispositionHeaderValue("form-data")
            {
                Name = "\"files\"",
                FileName = "\"" + fileName + "\""
            }; // the extra quotes are key here
            fileContent.Headers.ContentType = new MediaTypeHeaderValue(contentType);
            return fileContent;
        }

        public List<(Stream Stream, string FileName, string ContentType)> ConvertIFormFilesToStreams(List<IFormFile> files)
        {
            List<(Stream Stream, string FileName, string ContentType)> fileStreams = new List<(Stream, string, string)>();

            foreach (var file in files)
            {
                Stream stream = file.OpenReadStream(); // Open the IFormFile and copy its contents  --- to the memory stream
                string fileName = file.FileName; // Get the file name from the IFormFile
                string contentType = file.ContentType; // Get the MIME type from the IFormFile

                //file.CopyTo(stream);

                fileStreams.Add((stream, fileName, contentType));
            }

            return fileStreams;
        }

    }
}
