using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.IO;
using System.IO.Compression;
using System.Net.Http.Headers;
using System.Reflection;
using static System.Net.Mime.MediaTypeNames;

namespace PPP_PAI_OiRPOS.Pages
{
    public class DetectionMultipleModel : PageModel
    {
        private readonly ILogger<DetectionMultipleModel> _logger;

        public string ErrorMessage { get; set; }
        public List<(string, string)> Images { get; set; }

        [BindProperty]
        public List<IFormFile> Files { get; set; }

        [BindProperty]
        public string Model { get; set; }

        public DetectionMultipleModel(ILogger<DetectionMultipleModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }

        public async Task<IActionResult> OnPost()
        {
            string model = Model;
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

                var streams = ConvertIFormFilesToStreams(files);
                foreach(var stream in streams)
                {
                    form.Add(CreateFileContent(stream.Stream, stream.FileName, stream.ContentType), "files");
                }

                _logger.LogInformation("Sending Post Async to Flask");
                var response = await client.PostAsync("/detectMulti", form);

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
