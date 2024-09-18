import os
import subprocess
import sys
import platform
import time
import shutil
import shlex

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

def create_extension_project(extension_name):
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

    # Construct the command with correct flags
    command = f'"{node_path}" "{yo_path}" code --type=ext-language-server --extensionName="{extension_name}" --extensionDisplayName="{extension_name}" --extensionDescription="A new VSCode extension" --extensionIdentifier="{identifier}" --gitInit=false --pkgManager=npm'
    
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
    """Set up the environment based on the language chosen."""
    if language == "python":
        setup_python_environment()
    elif language in ["javascript", "typescript"]:
        setup_js_environment(language)
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
    else:
        print("Unsupported language.")
        sys.exit(1)

def setup_python_environment():
    """Set up the Python environment."""
    print("Setting up Python environment...")
    # You can add Python-specific setup code here if needed

def setup_js_environment(language):
    """Set up the JavaScript/TypeScript environment."""
    print(f"Setting up {language} environment...")
    install_node()
    install_yeoman_and_generator()

def create_server_code(language):
    """Create server code based on the specified language."""
    if language == "ruby":
        create_ruby_server_code()
    elif language == "php":
        create_php_server_code()
    elif language == "go":
        create_go_server_code()
    elif language == "python":
        create_python_server_code()
    elif language in ["javascript", "typescript"]:
        create_js_server_code(language)
    elif language == "c#":
        create_csharp_server_code()
    elif language == "java":
        create_java_server_code()
    else:
        print("Unsupported language.")
        sys.exit(1)

def create_ruby_server_code():
    """Create a basic Ruby server code."""
    server_code = """
require 'webrick'

server = WEBrick::HTTPServer.new :Port => 8000, :DocumentRoot => Dir.pwd

server.mount_proc '/' do |req, res|
  res.body = 'Hello, Ruby server!'
end

trap 'INT' do server.shutdown end

server.start
"""
    with open("server.rb", "w") as file:
        file.write(server_code)

def create_php_server_code():
    """Create a basic PHP server code."""
    server_code = """
<?php
// A basic PHP server script
echo "Hello, PHP server!";
?>
"""
    with open("server.php", "w") as file:
        file.write(server_code)

def create_go_server_code():
    """Create a basic Go server code."""
    server_code = """
package main

import (
    "fmt"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, Go server!")
}

func main() {
    http.HandleFunc("/", handler)
    http.ListenAndServe(":8080", nil)
}
"""
    with open("server.go", "w") as file:
        file.write(server_code)

def create_python_server_code():
    """Create a basic Python server code."""
    server_code = """
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Python server!'

if __name__ == '__main__':
    app.run(debug=True)
"""
    with open("server.py", "w") as file:
        file.write(server_code)

def create_js_server_code(language):
    """Create a basic JavaScript or TypeScript server code."""
    if language == "javascript":
        server_code = """
const http = require('http');

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello, JavaScript server!');
});

server.listen(3000, () => {
  console.log('Server running at http://127.0.0.1:3000/');
});
"""
        with open("server.js", "w") as file:
            file.write(server_code)
    elif language == "typescript":
        server_code = """
import * as http from 'http';

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello, TypeScript server!');
});

server.listen(3000, () => {
  console.log('Server running at http://127.0.0.1:3000/');
});
"""
        with open("server.ts", "w") as file:
            file.write(server_code)

def create_csharp_server_code():
    """Create a basic C# server code."""
    server_code = """
using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public class Program
{
    public static async Task Main(string[] args)
    {
        var host = Host.CreateDefaultBuilder(args)
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.Configure(app =>
                {
                    app.Run(async context =>
                    {
                        await context.Response.WriteAsync("Hello, C# server!");
                    });
                });
            })
            .Build();

        await host.RunAsync();
    }
}
"""
    with open("Program.cs", "w") as file:
        file.write(server_code)

def create_java_server_code():
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
        language = input("Enter the language for the server (python, javascript, typescript, c#, java, ruby, php, go): ").strip().lower()
        
        try:
            setup_environment_for_language(language)
        except Exception as e:
            print(f"Error setting up environment: {e}")
            return True

        create_extension_project(extension_name)
        
        try:
            create_server_code(language)
        except Exception as e:
            print(f"Error creating server code: {e}")
            return True

        print("Setup complete!")
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
        user_input = input(f"{current_dir}> ")
        if not process_command(user_input):
            break

    print("Thank you for using VSCode Extension Creator!")

if __name__ == "__main__":
    main()