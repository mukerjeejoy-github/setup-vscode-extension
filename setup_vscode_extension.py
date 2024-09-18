import os
import subprocess
import sys
import platform
import time
import shutil
import shlex

LANGUAGE_FRAMEWORKS = {
    "python": ["Flask", "Django", "FastAPI"],
    "javascript": ["Express", "Koa", "Hapi"],
    "typescript": ["Express", "Nest.js", "Koa"],
    "c#": ["ASP.NET Core", "Nancy"],
    "java": ["Spring Boot", "Quarkus", "Micronaut"],
    "ruby": ["Ruby on Rails", "Sinatra"],
    "php": ["Laravel", "Symfony", "Slim"],
    "go": ["Gin", "Echo", "Fiber"]
}

def run_command(command, cwd=None, stream_output=False):
    """Run a shell command and print its output."""
    if platform.system() == "Windows":
        command = command.replace("/", "\\")
    print(f"Running command: {command}")
    
    if stream_output:
        process = subprocess.Popen(command, shell=True, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="ignore")
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        return process.poll()
    else:
        result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True, encoding="utf-8", errors="ignore")
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr, file=sys.stderr)
        return result.returncode

def install_package(package_name, install_command):
    """Install a package if it is not already installed."""
    if shutil.which(package_name) is None:
        print(f"{package_name} is not installed. Installing...")
        result = run_command(install_command, stream_output=True)
        if result != 0:
            print(f"Failed to install {package_name}.")
            sys.exit(result)
    else:
        print(f"{package_name} is already installed.")

def check_and_install_dotnet():
    """Check if dotnet is installed, and if not, install it."""
    if shutil.which("dotnet") is None:
        print("dotnet is not installed. Installing dotnet...")
        if platform.system() == "Windows":
            dotnet_url = "https://download.visualstudio.microsoft.com/download/pr/5b53e378-9dd8-4a8e-8c1f-8e37a58079c0/36e2b99aecc0d8b1e79dc49e678338d6/dotnet-sdk-6.0.414-win-x64.zip"
            dotnet_zip = "dotnet-sdk-6.0.414-win-x64.zip"
            dotnet_dir = "dotnet-sdk-6.0.414-win-x64"
            run_command(f"curl -O {dotnet_url}", stream_output=True)
            run_command(f"tar -xzf {dotnet_zip}", stream_output=True)
            os.environ["PATH"] += os.pathsep + os.path.abspath(dotnet_dir + "/dotnet")
            run_command(f"setx PATH \"%PATH%;{os.path.abspath(dotnet_dir + '/dotnet')}\"", stream_output=True)
        elif platform.system() == "Linux":
            install_package("dotnet", "wget https://download.visualstudio.microsoft.com/download/pr/23a2d5e5-8e30-41db-91e2-4d4336f132c2/95f0c1ab08c4dd7795b1f8f75f527c29/dotnet-sdk-6.0.414-linux-x64.tar.gz && sudo mkdir -p /usr/share/dotnet && sudo tar zxf dotnet-sdk-6.0.414-linux-x64.tar.gz -C /usr/share/dotnet && sudo ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet")
        elif platform.system() == "Darwin":
            install_package("dotnet", "brew install --cask dotnet-sdk")
        else:
            print("Unsupported operating system for automatic .NET installation.")
            sys.exit(1)
    else:
        print("dotnet is already installed.")

def install_node():
    """Install Node.js if not already installed."""
    install_package("node", "nvm install node")

def install_yeoman_and_generator():
    """Install Yeoman and VSCode Extension Generator."""
    print("Installing Yeoman and VSCode Extension Generator...")
    result = run_command("npm install -g yo generator-code", stream_output=True)
    if result != 0:
        print("Failed to install Yeoman and generator-code.")
        sys.exit(result)
    
    # Verify installation
    yo_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "npm", "node_modules", "yo", "lib", "cli.js")
    if os.path.exists(yo_path):
        print(f"Yeoman installed successfully at: {yo_path}")
    else:
        print("Yeoman installation not found. Please check your npm configuration.")
        sys.exit(1)
    
    print("Yeoman and VSCode Extension Generator installed successfully.")

def install_maven():
    """Check if Maven is installed, and if not, install it."""
    if shutil.which("mvn") is None:
        print("Maven is not installed. Installing Maven...")
        if platform.system() == "Windows":
            maven_url = "https://archive.apache.org/dist/maven/maven-3/3.8.8/binaries/apache-maven-3.8.8-bin.zip"
            maven_zip = "apache-maven-3.8.8-bin.zip"
            maven_dir = "apache-maven-3.8.8"
            run_command(f"curl -O {maven_url}", stream_output=True)
            run_command(f"unzip {maven_zip}", stream_output=True)
            os.environ["PATH"] += os.pathsep + os.path.abspath(maven_dir + "/bin")
            run_command(f"setx PATH \"%PATH%;{os.path.abspath(maven_dir + '/bin')}\"", stream_output=True)
        elif platform.system() == "Linux":
            install_package("mvn", "sudo apt-get update && sudo apt-get install -y maven")
        elif platform.system() == "Darwin":
            install_package("maven", "brew install maven")
        else:
            print("Unsupported operating system for automatic Maven installation.")
            sys.exit(1)
    else:
        print("Maven is already installed.")

def install_ruby():
    """Check if Ruby is installed, and if not, install it."""
    if shutil.which("ruby") is None:
        print("Ruby is not installed. Installing Ruby...")
        if platform.system() == "Windows":
            ruby_url = "https://rubyinstaller.org/downloads/rubyinstaller-3.2.1-1-x64.exe"
            ruby_installer = "rubyinstaller-3.2.1-1-x64.exe"
            run_command(f"curl -O {ruby_url}", stream_output=True)
            run_command(f"{ruby_installer}", stream_output=True)
        elif platform.system() == "Linux":
            install_package("ruby", "sudo apt-get update && sudo apt-get install -y ruby-full")
        elif platform.system() == "Darwin":
            install_package("ruby", "brew install ruby")
        else:
            print("Unsupported operating system for automatic Ruby installation.")
            sys.exit(1)
    else:
        print("Ruby is already installed.")

def install_php():
    """Check if PHP is installed, and if not, install it."""
    if shutil.which("php") is None:
        print("PHP is not installed. Installing PHP...")
        if platform.system() == "Windows":
            php_url = "https://windows.php.net/downloads/releases/php-8.1.11-Win32-vs16-x64.zip"
            php_zip = "php-8.1.11-Win32-vs16-x64.zip"
            php_dir = "php-8.1.11-Win32-vs16-x64"
            run_command(f"curl -O {php_url}", stream_output=True)
            run_command(f"unzip {php_zip}", stream_output=True)
            os.environ["PATH"] += os.pathsep + os.path.abspath(php_dir + "/")
            run_command(f"setx PATH \"%PATH%;{os.path.abspath(php_dir)}\"", stream_output=True)
        elif platform.system() == "Linux":
            install_package("php", "sudo apt-get update && sudo apt-get install -y php")
        elif platform.system() == "Darwin":
            install_package("php", "brew install php")
        else:
            print("Unsupported operating system for automatic PHP installation.")
            sys.exit(1)
    else:
        print("PHP is already installed.")

def install_go():
    """Check if Go is installed, and if not, install it."""
    if shutil.which("go") is None:
        print("Go is not installed. Installing Go...")
        if platform.system() == "Windows":
            go_url = "https://golang.org/dl/go1.20.3.windows-amd64.msi"
            run_command(f"curl -O {go_url}", stream_output=True)
        elif platform.system() == "Linux":
            install_package("go", "sudo apt-get update && sudo apt-get install -y golang")
        elif platform.system() == "Darwin":
            install_package("go", "brew install go")
        else:
            print("Unsupported operating system for automatic Go installation.")
            sys.exit(1)
    else:
        print("Go is already installed.")

def generate_extension_name_and_identifier(extension_name):
    """Automatically generate the extension name and identifier."""
    identifier = extension_name.lower().replace(" ", "-")
    return extension_name, identifier

def create_extension_project(extension_name, extension_description):
    """Generate a new VSCode extension project using Yeoman."""
    print(f"Creating VSCode extension project '{extension_name}'...")
    try:
        os.makedirs(extension_name, exist_ok=True)
        os.chdir(extension_name)
    except Exception as e:
        print(f"Error creating or changing to directory: {e}")
        return

    extension_name, identifier = generate_extension_name_and_identifier(extension_name)
    
    print(f"Generated extension name: {extension_name}")
    print(f"Generated extension identifier: {identifier}")
    
    # Use Node.js to run Yeoman
    node_path = shutil.which("node")
    if node_path is None:
        print("Error: Node.js not found. Please ensure Node.js is installed and in your PATH.")
        return

    yo_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "npm", "node_modules", "yo", "lib", "cli.js")
    if not os.path.exists(yo_path):
        print(f"Error: Yeoman CLI not found at expected path: {yo_path}")
        print("Please ensure Yeoman is installed globally using 'npm install -g yo generator-code'")
        return

    # Construct the command with correct flags, including the description
    command = f'"{node_path}" "{yo_path}" code --type=ext-language-server --extensionName="{extension_name}" --extensionDisplayName="{extension_name}" --extensionDescription="{extension_description}" --extensionIdentifier="{identifier}" --gitInit=false --pkgManager=npm'
    
    print(f"Executing command: {command}")

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
        
        output = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                print(line.strip())
                output.append(line.strip())

        if process.returncode != 0:
            print(f"Yeoman process exited with non-zero status: {process.returncode}")
            print("Last few lines of output:")
            print("\n".join(output[-10:]))  # Print the last 10 lines of output
            return

        print("VSCode extension project created successfully.")
    except Exception as e:
        print(f"Error during extension project creation: {e}")
        return

    print("Project creation completed.")

def setup_environment_for_language(language):
    """Set up the environment based on the language chosen and select a framework."""
    if language not in LANGUAGE_FRAMEWORKS:
        print("Unsupported language.")
        sys.exit(1)
    
    print(f"\nAvailable frameworks for {language}:")
    for i, framework in enumerate(LANGUAGE_FRAMEWORKS[language], 1):
        print(f"{i}. {framework}")
    
    while True:
        choice = input("\nSelect a framework (enter the number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(LANGUAGE_FRAMEWORKS[language]):
                framework = LANGUAGE_FRAMEWORKS[language][index]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nSelected framework: {framework}")
    
    if language == "python":
        setup_python_environment(framework)
    elif language in ["javascript", "typescript"]:
        setup_js_environment(language, framework)
    elif language == "c#":
        check_and_install_dotnet()
    elif language == "java":
        install_maven()
    elif language == "ruby":
        install_ruby()
    elif language == "php":
        install_php()
    elif language == "go":
        install_go()
    
    return framework

def setup_python_environment():
    """Set up the Python environment."""
    print("Setting up Python environment...")
    # You can add Python-specific setup code here if needed

def setup_js_environment(language):
    """Set up the JavaScript/TypeScript environment."""
    print(f"Setting up {language} environment...")
    install_node()
    install_yeoman_and_generator()

def create_server_code(language, framework):
    """Create server code based on the specified language and framework."""
    if language == "python":
        create_python_server_code(framework)
    elif language in ["javascript", "typescript"]:
        create_js_server_code(language, framework)
    elif language == "c#":
        create_csharp_server_code(framework)
    elif language == "java":
        create_java_server_code(framework)
    elif language == "ruby":
        create_ruby_server_code(framework)
    elif language == "php":
        create_php_server_code(framework)
    elif language == "go":
        create_go_server_code(framework)
    else:
        print(f"Unsupported language: {language}")
        sys.exit(1)

def create_python_server_code(framework):
    """Create a Python server code based on the selected framework."""
    if framework == "Flask":
        server_code = """
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask server!'

if __name__ == '__main__':
    app.run(debug=True)
"""
    elif framework == "Django":
        server_code = """
# myproject/urls.py
from django.http import HttpResponse
from django.urls import path

def hello(request):
    return HttpResponse("Hello, Django server!")

urlpatterns = [
    path('', hello, name='hello'),
]

# Note: You'll need to set up a proper Django project structure
"""
    elif framework == "FastAPI":
        server_code = """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI server!"}
"""
    else:
        server_code = f"# Add {framework}-specific code here"

    with open("server.py", "w") as file:
        file.write(server_code)

def create_js_server_code(language, framework):
    """Create a JavaScript or TypeScript server code based on the selected framework."""
    if framework == "Express":
        server_code = """
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello, Express server!');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
"""
    elif framework == "Koa":
        server_code = """
const Koa = require('koa');
const app = new Koa();

app.use(async ctx => {
  ctx.body = 'Hello, Koa server!';
});

app.listen(3000);
"""
    elif framework == "Hapi":
        server_code = """
const Hapi = require('@hapi/hapi');

const init = async () => {
    const server = Hapi.server({
        port: 3000,
        host: 'localhost'
    });

    server.route({
        method: 'GET',
        path: '/',
        handler: (request, h) => {
            return 'Hello, Hapi server!';
        }
    });

    await server.start();
    console.log('Server running on %s', server.info.uri);
};

process.on('unhandledRejection', (err) => {
    console.log(err);
    process.exit(1);
});

init();
"""
    elif framework == "Nest.js":
        server_code = """
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();
"""
    else:
        server_code = f"// Add {framework}-specific code here"

    file_extension = "ts" if language == "typescript" else "js"
    with open(f"server.{file_extension}", "w") as file:
        file.write(server_code)

def create_csharp_server_code(framework):
    """Create a C# server code based on the selected framework."""
    if framework == "ASP.NET Core":
        server_code = """
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;

public class Program
{
    public static void Main(string[] args)
    {
        CreateHostBuilder(args).Build().Run();
    }

    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.Configure(app =>
                {
                    app.UseRouting();
                    app.UseEndpoints(endpoints =>
                    {
                        endpoints.MapGet("/", async context =>
                        {
                            await context.Response.WriteAsync("Hello, ASP.NET Core server!");
                        });
                    });
                });
            });
}
"""
    elif framework == "Nancy":
        server_code = """
using Nancy;
using Nancy.Hosting.Self;

public class HelloModule : NancyModule
{
    public HelloModule()
    {
        Get("/", _ => "Hello, Nancy server!");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        using (var host = new NancyHost(new Uri("http://localhost:3000")))
        {
            host.Start();
            Console.WriteLine("Nancy server running on http://localhost:3000");
            Console.ReadLine();
        }
    }
}
"""
    else:
        server_code = f"// Add {framework}-specific code here"

    with open("Program.cs", "w") as file:
        file.write(server_code)

def create_java_server_code(framework):
    """Create a Java server code based on the selected framework."""
    if framework == "Spring Boot":
        server_code = """
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

    @GetMapping("/")
    public String hello() {
        return "Hello, Spring Boot server!";
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
"""
    elif framework == "Quarkus":
        server_code = """
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/")
public class GreetingResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String hello() {
        return "Hello, Quarkus server!";
    }
}
"""
    elif framework == "Micronaut":
        server_code = """
import io.micronaut.http.annotation.*;
import io.micronaut.http.MediaType;

@Controller("/")
public class HelloController {

    @Get(produces = MediaType.TEXT_PLAIN)
    public String index() {
        return "Hello, Micronaut server!";
    }
}
"""
    else:
        server_code = f"// Add {framework}-specific code here"

    with open("Application.java", "w") as file:
        file.write(server_code)

def create_ruby_server_code(framework):
    """Create a Ruby server code based on the selected framework."""
    if framework == "Ruby on Rails":
        server_code = """
# config/routes.rb
Rails.application.routes.draw do
  root 'application#hello'
end

# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  def hello
    render plain: "Hello, Ruby on Rails server!"
  end
end
"""
    elif framework == "Sinatra":
        server_code = """
require 'sinatra'

get '/' do
  'Hello, Sinatra server!'
end
"""
    else:
        server_code = f"# Add {framework}-specific code here"

    with open("server.rb", "w") as file:
        file.write(server_code)

def create_php_server_code(framework):
    """Create a PHP server code based on the selected framework."""
    if framework == "Laravel":
        server_code = """
<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return 'Hello, Laravel server!';
});
"""
    elif framework == "Symfony":
        server_code = """
<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class HelloController
{
    #[Route('/')]
    public function index(): Response
    {
        return new Response('Hello, Symfony server!');
    }
}
"""
    elif framework == "Slim":
        server_code = """
<?php

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\Factory\AppFactory;

require __DIR__ . '/vendor/autoload.php';

$app = AppFactory::create();

$app->get('/', function (Request $request, Response $response, $args) {
    $response->getBody()->write("Hello, Slim server!");
    return $response;
});

$app->run();
"""
    else:
        server_code = f"<?php\n// Add {framework}-specific code here\n"

    with open("server.php", "w") as file:
        file.write(server_code)

def create_go_server_code(framework):
    """Create a Go server code based on the selected framework."""
    if framework == "Gin":
        server_code = """
package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	r := gin.Default()
	r.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "Hello, Gin server!")
	})
	r.Run()
}
"""
    elif framework == "Echo":
        server_code = """
package main

import (
	"github.com/labstack/echo/v4"
	"net/http"
)

func main() {
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, Echo server!")
	})
	e.Logger.Fatal(e.Start(":8080"))
}
"""
    elif framework == "Fiber":
        server_code = """
package main

import "github.com/gofiber/fiber/v2"

func main() {
    app := fiber.New()

    app.Get("/", func(c *fiber.Ctx) error {
        return c.SendString("Hello, Fiber server!")
    })

    app.Listen(":3000")
}
"""
    else:
        server_code = f"// Add {framework}-specific code here"

    with open("server.go", "w") as file:
        file.write(server_code)
    """Create a basic Java server code."""
    server_code = """
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class SimpleHttpServer {

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                String response = "Hello, Java server!";
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            }
        });
        server.start();
    }
}
"""
    with open("SimpleHttpServer.java", "w") as file:
        file.write(server_code)


def process_command(command):
    """Process user commands."""
    if command.lower() == 'exit':
        return False
    elif command.lower() == 'create':
        # Run the extension creation process
        extension_name = input("Enter the extension name: ")
        extension_description = input("Enter a brief description of the extension: ")
        
        print("\nAvailable languages:")
        for i, lang in enumerate(LANGUAGE_FRAMEWORKS.keys(), 1):
            print(f"{i}. {lang}")
        
        while True:
            lang_choice = input("\nSelect a language (enter the number): ")
            try:
                lang_index = int(lang_choice) - 1
                if 0 <= lang_index < len(LANGUAGE_FRAMEWORKS):
                    language = list(LANGUAGE_FRAMEWORKS.keys())[lang_index]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\nSelected language: {language}")
        
        try:
            framework = setup_environment_for_language(language)
        except Exception as e:
            print(f"Error setting up environment: {e}")
            return True

        create_extension_project(extension_name, extension_description)
        
        try:
            create_server_code(language, framework)
        except Exception as e:
            print(f"Error creating server code: {e}")
            return True

        print("\nSetup complete!")
    else:
        # Execute the command in the current process
        try:
            args = shlex.split(command)
            if args[0] == 'cd':
                if len(args) > 1:
                    os.chdir(args[1])
                else:
                    print(f"Current directory: {os.getcwd()}")
            elif args[0] == 'pwd':
                print(os.getcwd())
            else:
                os.system(command)
        except FileNotFoundError:
            print(f"Directory not found: {args[1]}")
        except PermissionError:
            print(f"Permission denied: {args[1]}")
        except Exception as e:
            print(f"Error executing command: {e}")
    return True

def main():
    print("Welcome to the VSCode Extension Creator Command Prompt!")
    print("Available custom commands:")
    print("  create  - Start the extension creation process")
    print("  cd      - Change directory")
    print("  pwd     - Print working directory")
    print("  exit    - Exit the program")
    print("All standard system commands are also available.")
    
    while True:
        current_dir = os.getcwd()
        user_input = input(f"\n{current_dir}> ")
        if not process_command(user_input):
            break

    print("Thank you for using VSCode Extension Creator!")

if __name__ == "__main__":
    main()