using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using PPP_PAI_OiRPOS.Pages;
using System.Net.Http;

namespace PPP_PAI_OiRPOS.Pages
{
    public class DetectionModel : PageModel
    {
        private readonly ILogger<DetectionModel> _logger;

        [BindProperty]
        public IFormFile File { get; set; }

        [BindProperty]
        public string Model { get; set; }

        public string ErrorMessage { get; set; }
        public string Image {  get; set; }

        public DetectionModel(ILogger<DetectionModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
        }

        public async Task<IActionResult> OnPost() 
        {
            _logger.LogInformation("Detection OnPost()");
            // Process form data
            string model = Model; // Get the selected model
            IFormFile file = File; // Get the uploaded file
            ErrorMessage = "";

            if (file != null && file.Length > 0)
            {
                using (var client = new HttpClient())
                {
                    // Define the base URL of the server on another port
                    client.BaseAddress = new Uri("http://localhost:8000");

                    // Create a FormDataContent to send the file and model as form data
                    var form = new MultipartFormDataContent();
                    form.Add(new StringContent(model), "model");
                    form.Add(new StreamContent(file.OpenReadStream()), "file", file.FileName);

                    // Send the POST request
                    _logger.LogInformation("Sending Post Async to Flask");
                    var response = await client.PostAsync("/detect", form);
                    _logger.LogInformation("Revcivig result form Async to Flask");

                    if (response.IsSuccessStatusCode)
                    {
                        // The request was successful
                        // You can handle the response as needed
                        // Get the image data as a stream

                        //var imageStream = await response.Content.ReadAsStreamAsync();
                        // Return the image data to the user as a downloadable image
                        //return File(imageStream, "image/jpeg", "output.jpg"); // Change the file name and media type as needed

                        var imageBytes = await response.Content.ReadAsByteArrayAsync();
                        var base64Image = Convert.ToBase64String(imageBytes);
                        Image = $"data:image/jpeg;base64,{base64Image}";
                        return Page();
                        }
                    else
                    {
                        // Handle the case where the request was not successful
                        // You can check response.StatusCode for specific error codes
                        ErrorMessage = response.StatusCode.ToString();
                    }
                }
            }
            else
            {
                ErrorMessage = "File is missing";
            }
            return Page();
        }
    }
}
