using Microsoft.AspNetCore.Mvc;
using System.Net;
using System.Text.RegularExpressions;

namespace CurrentWind.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet(Name = "GetWeatherForecast")]
        public async Task<WeatherForecast> Get(string station)
        {
            int num = -1;
            try
            {
                var client = new HttpClient();
                //folly station = fbis1
                var response = await client.GetAsync("http://www.ndbc.noaa.gov/station_page.php?station=" + station);
                var responseContent = await response.Content.ReadAsStringAsync();
                    
                Match match = Regex.Match(responseContent, "Continuous Winds((.|\\r|\\n)(?!\\d+\\skts))*\\s*((\\d+)\\s+kts)");
                if (match.Success)
                {
                    num = int.Parse(match.Groups[4].Value);
                }               
            }
            catch
            {
            }

            return new WeatherForecast
            {
                Date = DateTime.Now,
                WindSpeed = num
            };
        }
    }
}