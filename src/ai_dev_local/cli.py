import click
import subprocess
import sys

@click.group()
def cli():
    """AI Dev Local - Manage your AI development environment."""
    pass

@cli.command()
@click.option('--ollama', is_flag=True, help='Include Ollama service')
@click.option('--build', is_flag=True, help='Build images before starting')
def start(ollama, build):
    """Start all AI Dev Local services."""
    click.echo("🚀 Starting AI Dev Local services...")
    
    # Get git version for dashboard
    import os
    try:
        git_tag = subprocess.run(['git', 'describe', '--tags', '--always'], 
                                capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        git_tag = 'v0.2.1'
    
    # Get build date
    import datetime
    build_date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Set environment variables
    env = os.environ.copy()
    env['GIT_TAG'] = git_tag
    env['BUILD_DATE'] = build_date
    
    click.echo(f"📋 Version: {git_tag}")
    click.echo(f"📅 Build Date: {build_date}")
    
    cmd = ['docker-compose']
    
    if ollama:
        cmd.extend(['--profile', 'ollama'])
    
    cmd.append('up')
    
    if build:
        cmd.append('--build')
    
    cmd.extend(['-d'])
    
    try:
        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
        click.echo("✅ Services started successfully!")
        click.echo("\n📋 Service URLs:")
        
        # Get host and port configurations from environment
        host = env.get('HOST', 'localhost')
        dashboard_port = env.get('DASHBOARD_PORT', '3002')
        langfuse_port = env.get('LANGFUSE_PORT', '3000')
        flowise_port = env.get('FLOWISE_PORT', '3001')
        openwebui_port = env.get('OPENWEBUI_PORT', '8081')
        litellm_port = env.get('LITELLM_PORT', '4000')
        mkdocs_port = env.get('MKDOCS_PORT', '8000')
        
        click.echo(f"  • Dashboard: http://{host}:{dashboard_port}")
        click.echo(f"  • Langfuse: http://{host}:{langfuse_port}")
        click.echo(f"  • FlowiseAI: http://{host}:{flowise_port}")
        click.echo(f"  • Open WebUI: http://{host}:{openwebui_port}")
        click.echo(f"  • LiteLLM Proxy: http://{host}:{litellm_port}")
        click.echo(f"  • Documentation: http://{host}:{mkdocs_port}")
        if ollama:
            ollama_port = env.get('OLLAMA_PORT', '11434')
            click.echo(f"  • Ollama: http://{host}:{ollama_port}")
        
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to start services: {e.stderr}", err=True)
        sys.exit(1)

@cli.command()
def stop():
    """Stop all AI Dev Local services."""
    click.echo("🛑 Stopping AI Dev Local services...")
    
    try:
        subprocess.run(['docker-compose', 'down'], check=True, capture_output=True)
        click.echo("✅ Services stopped successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to stop services: {e}", err=True)
        sys.exit(1)

@cli.command()
def status():
    """Show status of all services."""
    click.echo("📊 Service Status:")
    
    try:
        result = subprocess.run(['docker-compose', 'ps'], check=True, capture_output=True, text=True)
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to get status: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('service', required=False)
def logs(service):
    """Show logs for services."""
    cmd = ['docker-compose', 'logs']
    
    if service:
        cmd.append(service)
        click.echo(f"📋 Logs for {service}:")
    else:
        click.echo("📋 Logs for all services:")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to get logs: {e}", err=True)
        sys.exit(1)

@cli.command()
def docs():
    """Open documentation in browser."""
    import webbrowser
    import os
    
    host = os.getenv('HOST', 'localhost')
    mkdocs_port = os.getenv('MKDOCS_PORT', '8000')
    click.echo("📚 Opening documentation...")
    webbrowser.open(f'http://{host}:{mkdocs_port}')

@cli.command('docs-reload')
def docs_reload():
    """Reload/update MkDocs documentation service."""
    click.echo("📚 Updating MkDocs documentation...")
    
    # Check if MkDocs service is running
    try:
        result = subprocess.run(['docker-compose', 'ps', 'mkdocs'], 
                              capture_output=True, text=True, check=True)
        if 'Up' not in result.stdout:
            click.echo("❌ MkDocs service is not running. Start it first with: ai-dev-local start")
            sys.exit(1)
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to check MkDocs status")
        sys.exit(1)
    
    try:
        # Stop the MkDocs service first
        click.echo("🛑 Stopping MkDocs service...")
        subprocess.run(['docker-compose', 'stop', 'mkdocs'], check=True, capture_output=True)
        
        # Rebuild the MkDocs Docker image to pick up documentation changes
        click.echo("🔨 Rebuilding MkDocs Docker image...")
        subprocess.run(['docker-compose', 'build', 'mkdocs'], check=True, capture_output=True)
        
        # Start the service with the new image
        click.echo("🚀 Starting MkDocs service with updated documentation...")
        subprocess.run(['docker-compose', 'up', '-d', 'mkdocs'], check=True, capture_output=True)
        
        click.echo("✅ MkDocs documentation updated successfully!")
        
        # Show documentation URL
        import os
        host = os.getenv('HOST', 'localhost')
        mkdocs_port = os.getenv('MKDOCS_PORT', '8000')
        click.echo(f"📖 Documentation available at: http://{host}:{mkdocs_port}")
        
        # Ask if user wants to open in browser
        if click.confirm("🌐 Open documentation in browser?"):
            import webbrowser
            webbrowser.open(f'http://{host}:{mkdocs_port}')
        
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to reload MkDocs: {e}", err=True)
        sys.exit(1)

@cli.command()
def dashboard():
    """Open dashboard in browser."""
    import webbrowser
    import os
    
    host = os.getenv('HOST', 'localhost')
    dashboard_port = os.getenv('DASHBOARD_PORT', '3002')
    click.echo("🎛️ Opening dashboard...")
    webbrowser.open(f'http://{host}:{dashboard_port}')

@cli.command()
def version():
    """Display current version from git tag."""
    try:
        # Try to get version from git tag
        result = subprocess.run(['git', 'describe', '--tags', '--exact-match'], 
                              capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        click.echo(f"🏷️  Current Version: {version}")
    except subprocess.CalledProcessError:
        try:
            # Fallback to latest tag with commit info
            result = subprocess.run(['git', 'describe', '--tags', '--always'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            click.echo(f"🏷️  Current Version: {version} (development)")
        except subprocess.CalledProcessError:
            # Final fallback to __init__.py version
            from ai_dev_local import __version__
            click.echo(f"🏷️  Current Version: {__version__} (no git tags found)")

@cli.group()
def mcp():
    """Manage MCP services."""
    pass

@mcp.command()
def start():
    """Start MCP servers using docker-compose.mcp.yml."""
    click.echo("🚀 Starting MCP servers...")
    try:
        subprocess.run(['docker-compose', '-p', 'ai-dev-mcp', '-f', 'docker-compose.mcp.yml', '--env-file', '.env', 'up', '-d'], check=True)
        click.echo("✅ MCP servers started successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to start MCP servers: {e}", err=True)

@mcp.command()
def stop():
    """Stop MCP servers using docker-compose.mcp.yml."""
    click.echo("🛑 Stopping MCP servers...")
    try:
        subprocess.run(['docker-compose', '-p', 'ai-dev-mcp', '-f', 'docker-compose.mcp.yml', 'down'], check=True)
        click.echo("✅ MCP servers stopped successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to stop MCP servers: {e}", err=True)

@mcp.command()
def status():
    """Show status of MCP servers using docker-compose.mcp.yml."""
    click.echo("📊 MCP Server Status:")
    try:
        cmd = ['docker-compose', '-p', 'ai-dev-mcp', '-f', 'docker-compose.mcp.yml', 'ps']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        # Check if output contains only the header (meaning no services)
        lines = result.stdout.strip().split('\n')
        if len(lines) <= 1 or (len(lines) == 1 and 'NAME' in lines[0]):
            click.echo("ℹ️ No MCP services are currently running.")
            click.echo("💡 Use 'ai-dev-local mcp start' to start MCP services.")
        else:
            click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to get MCP server status: {e}", err=True)
        if e.stderr:
            click.echo(f"Error details: {e.stderr}", err=True)

@cli.group()
def config():
    """Manage configuration and .env file."""
    pass

@config.command()
def init():
    """Initialize .env file from .env.example template."""
    import os
    import shutil
    
    env_example = '.env.example'
    env_file = '.env'
    
    if not os.path.exists(env_example):
        click.echo("❌ .env.example file not found", err=True)
        sys.exit(1)
    
    if os.path.exists(env_file):
        if not click.confirm(f"⚠️  {env_file} already exists. Overwrite?"):
            click.echo("✅ Configuration initialization cancelled")
            return
    
    try:
        shutil.copy2(env_example, env_file)
        click.echo(f"✅ Created {env_file} from {env_example}")
        click.echo("\n📝 Next steps:")
        click.echo("  1. Edit .env file with your API keys and settings")
        click.echo("  2. Use 'ai-dev-local config set' to update specific values")
        click.echo("  3. Use 'ai-dev-local config show' to view current settings")
    except Exception as e:
        click.echo(f"❌ Failed to create .env file: {e}", err=True)
        sys.exit(1)

@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set a configuration value in .env file."""
    import os
    import re
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        if click.confirm("📝 .env file doesn't exist. Create it from template?"):
            ctx = click.get_current_context()
            ctx.invoke(init)
        else:
            click.echo("❌ .env file is required", err=True)
            sys.exit(1)
    
    try:
        # Read current .env file
        with open(env_file, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        key_found = False
        updated_lines = []
        
        # Process each line to find and update the key
        for line in lines:
            # Check if this line contains our key (handle comments and whitespace)
            if re.match(rf'^\s*{re.escape(key)}\s*=', line):
                # Preserve any inline comments
                if '#' in line and '=' in line:
                    # Split on = first, then check for # in the value part
                    key_part, value_part = line.split('=', 1)
                    if '#' in value_part:
                        # Preserve the comment
                        comment_match = re.search(r'\s*#(.*)$', value_part)
                        if comment_match:
                            comment = comment_match.group(1)
                            updated_lines.append(f"{key}={value}  # {comment}")
                        else:
                            updated_lines.append(f"{key}={value}")
                    else:
                        updated_lines.append(f"{key}={value}")
                else:
                    updated_lines.append(f"{key}={value}")
                key_found = True
            else:
                updated_lines.append(line)
        
        # If key not found, add it in appropriate section or at the end
        if not key_found:
            # Try to find appropriate section to add the key
            section_added = False
            
            # Define key categories for intelligent placement
            api_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GEMINI_API_KEY', 'COHERE_API_KEY']
            host_port_keys = ['HOST', 'POSTGRES_PORT', 'REDIS_PORT', 'LANGFUSE_PORT', 'FLOWISE_PORT', 
                             'OPENWEBUI_PORT', 'LITELLM_PORT', 'OLLAMA_PORT', 'DASHBOARD_PORT', 'MKDOCS_PORT']
            
            if key in api_keys:
                # Add to LLM Provider API Keys section
                for i, line in enumerate(updated_lines):
                    if '# LLM Provider API Keys' in line:
                        # Find the end of this section
                        j = i + 1
                        while j < len(updated_lines) and not updated_lines[j].startswith('# ============='):
                            j += 1
                        # Insert before the next section
                        updated_lines.insert(j - 1, f"{key}={value}")
                        section_added = True
                        break
            elif key in host_port_keys:
                # Add to Host and Port Configuration section
                for i, line in enumerate(updated_lines):
                    if '# Host and Port Configuration' in line:
                        # Find the end of this section
                        j = i + 1
                        while j < len(updated_lines) and not updated_lines[j].startswith('# ============='):
                            j += 1
                        # Insert before the next section
                        updated_lines.insert(j - 1, f"{key}={value}")
                        section_added = True
                        break
            
            # If no appropriate section found, add at the end with a comment
            if not section_added:
                updated_lines.extend([
                    '',
                    '# Added by ai-dev-local config',
                    f'{key}={value}'
                ])
        
        # Write back to file
        with open(env_file, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        click.echo(f"✅ Set {key}={value}")
        
    except Exception as e:
        click.echo(f"❌ Failed to update .env file: {e}", err=True)
        sys.exit(1)

@config.command()
@click.argument('key', required=False)
def show(key):
    """Show configuration values from .env file."""
    import os
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        click.echo("❌ .env file not found. Run 'ai-dev-local config init' first.", err=True)
        sys.exit(1)
    
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        if key:
            # Show specific key
            for line in lines:
                if line.strip().startswith(f"{key}="):
                    value = line.split('=', 1)[1].strip()
                    # Mask sensitive values
                    if any(sensitive in key.upper() for sensitive in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                        if value and value != 'your-api-key-here' and not value.startswith('*'):
                            masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '*' * len(value)
                            click.echo(f"{key}={masked_value}")
                        else:
                            click.echo(f"{key}={value}")
                    else:
                        click.echo(f"{key}={value}")
                    return
            click.echo(f"❌ Key '{key}' not found in .env file")
        else:
            # Show all non-empty, non-comment lines
            click.echo("📋 Current configuration:")
            click.echo("=" * 50)
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key_part, value_part = line.split('=', 1)
                    # Mask sensitive values
                    if any(sensitive in key_part.upper() for sensitive in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                        if value_part and value_part != 'your-api-key-here' and not value_part.startswith('*'):
                            masked_value = value_part[:8] + '*' * (len(value_part) - 8) if len(value_part) > 8 else '*' * len(value_part)
                            click.echo(f"{key_part}={masked_value}")
                        else:
                            click.echo(f"{key_part}={value_part}")
                    else:
                        click.echo(f"{key_part}={value_part}")
            
    except Exception as e:
        click.echo(f"❌ Failed to read .env file: {e}", err=True)
        sys.exit(1)

@config.command()
def validate():
    """Validate .env file configuration."""
    import os
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        click.echo("❌ .env file not found. Run 'ai-dev-local config init' first.", err=True)
        sys.exit(1)
    
    try:
        # Define required and optional keys with their categories
        required_keys = {
            'OPENAI_API_KEY': 'OpenAI API access',
            'WEBUI_SECRET_KEY': 'Open WebUI security',
            'LITELLM_MASTER_KEY': 'LiteLLM proxy access'
        }
        
        optional_keys = {
            'ANTHROPIC_API_KEY': 'Claude models',
            'GEMINI_API_KEY': 'Google Gemini models',
            'COHERE_API_KEY': 'Cohere models',
            'LANGFUSE_PUBLIC_KEY': 'Langfuse observability',
            'LANGFUSE_SECRET_KEY': 'Langfuse observability'
        }
        
        # Read .env file
        env_vars = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        
        click.echo("🔍 Validating configuration...")
        click.echo("=" * 50)
        
        all_valid = True
        
        # Check required keys
        click.echo("\n📋 Required Settings:")
        for key, description in required_keys.items():
            value = env_vars.get(key, '')
            if not value or value in ['your-api-key-here', '*' * 20]:
                click.echo(f"  ❌ {key}: Missing or placeholder ({description})")
                all_valid = False
            else:
                click.echo(f"  ✅ {key}: Configured ({description})")
        
        # Check optional keys
        click.echo("\n🔧 Optional Settings:")
        for key, description in optional_keys.items():
            value = env_vars.get(key, '')
            if not value or value in ['your-api-key-here', '*' * 20]:
                click.echo(f"  ⚠️  {key}: Not configured ({description})")
            else:
                click.echo(f"  ✅ {key}: Configured ({description})")
        
        # Summary
        click.echo("\n" + "=" * 50)
        if all_valid:
            click.echo("✅ Configuration is valid! All required settings are present.")
        else:
            click.echo("❌ Configuration needs attention. Please set the missing required values.")
            click.echo("\n💡 Use 'ai-dev-local config set KEY VALUE' to update settings")
        
    except Exception as e:
        click.echo(f"❌ Failed to validate .env file: {e}", err=True)
        sys.exit(1)

@config.command()
@click.option('--category', '-c', help='Show only variables from specific category (api-keys, ports, services, mcp)')
def list(category):
    """List configuration variables by category."""
    import os
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        click.echo("❌ .env file not found. Run 'ai-dev-local config init' first.", err=True)
        sys.exit(1)
    
    # Define categories
    categories = {
        'api-keys': {
            'title': '🔑 LLM Provider API Keys',
            'keys': ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GEMINI_API_KEY', 'COHERE_API_KEY']
        },
        'ports': {
            'title': '🌐 Host and Port Configuration',
            'keys': ['HOST', 'POSTGRES_PORT', 'REDIS_PORT', 'LANGFUSE_PORT', 'FLOWISE_PORT', 
                    'OPENWEBUI_PORT', 'LITELLM_PORT', 'OLLAMA_PORT', 'DASHBOARD_PORT', 'MKDOCS_PORT']
        },
        'services': {
            'title': '⚙️ Service Configuration',
            'keys': ['TELEMETRY_ENABLED', 'DEBUG', 'LOG_LEVEL', 'WEBUI_SECRET_KEY', 'WEBUI_JWT_SECRET_KEY',
                    'LITELLM_MASTER_KEY', 'DASHBOARD_TITLE', 'OLLAMA_AUTO_PULL_MODELS', 'OLLAMA_GPU']
        },
            'mcp': {
                'title': '🤖 MCP (Model Context Protocol)',
                'keys': ['MCP_GATEWAY_PORT', 'MCP_GIT_PORT', 'MCP_FILESYSTEM_PORT', 'MCP_FETCH_PORT',
                        'MCP_MEMORY_PORT', 'MCP_TIME_PORT', 'MCP_POSTGRES_PORT', 'MCP_EVERYTHING_PORT',
                        'MCP_GITHUB_PORT', 'MCP_GITLAB_PORT', 'MCP_SONARQUBE_PORT', 
                        'GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'TIMEZONE', 'GITHUB_PERSONAL_ACCESS_TOKEN',
                        'GITLAB_TOKEN', 'SONARQUBE_URL', 'SONARQUBE_TOKEN']
            }
    }
    
    try:
        # Read .env file
        env_vars = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        
        if category:
            # Show specific category
            if category not in categories:
                click.echo(f"❌ Unknown category '{category}'. Available: {', '.join(categories.keys())}")
                sys.exit(1)
            
            cat_info = categories[category]
            click.echo(f"{cat_info['title']}")
            click.echo("=" * 50)
            
            for key in cat_info['keys']:
                value = env_vars.get(key, 'Not set')
                # Mask sensitive values
                if any(sensitive in key.upper() for sensitive in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                    if value != 'Not set' and value != 'your-api-key-here' and not value.startswith('*'):
                        masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '*' * len(value)
                        click.echo(f"  {key} = {masked_value}")
                    else:
                        click.echo(f"  {key} = {value}")
                else:
                    click.echo(f"  {key} = {value}")
        else:
            # Show all categories
            for cat_name, cat_info in categories.items():
                click.echo(f"\n{cat_info['title']}")
                click.echo("=" * 50)
                
                for key in cat_info['keys']:
                    value = env_vars.get(key, 'Not set')
                    # Mask sensitive values
                    if any(sensitive in key.upper() for sensitive in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                        if value != 'Not set' and value != 'your-api-key-here' and not value.startswith('*'):
                            masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '*' * len(value)
                            click.echo(f"  {key} = {masked_value}")
                        else:
                            click.echo(f"  {key} = {value}")
                    else:
                        click.echo(f"  {key} = {value}")
            
            click.echo("\n💡 Use --category to filter by: " + ", ".join(categories.keys()))
    
    except Exception as e:
        click.echo(f"❌ Failed to read .env file: {e}", err=True)
        sys.exit(1)

@config.command()
def edit():
    """Open .env file in default editor."""
    import os
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        if click.confirm("📝 .env file doesn't exist. Create it from template?"):
            ctx = click.get_current_context()
            ctx.invoke(init)
        else:
            click.echo("❌ .env file is required", err=True)
            sys.exit(1)
    
    # Try to open with various editors
    editors = [os.getenv('EDITOR'), 'code', 'nano', 'vim', 'vi']
    
    for editor in editors:
        if editor:
            try:
                click.echo(f"📝 Opening .env file with {editor}...")
                subprocess.run([editor, env_file], check=True)
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    # Fallback: show instructions
    click.echo("📝 Please edit the .env file manually:")
    click.echo(f"   {os.path.abspath(env_file)}")

@cli.group()
def ollama():
    """Manage Ollama local LLM server."""
    pass

@ollama.command()
@click.option('--models', help='Comma-separated list of models to pull (e.g., llama2:7b,codellama:7b)')
def init(models):
    """Initialize Ollama with common models."""
    click.echo("🚀 Initializing Ollama...")
    
    # Check if Ollama service is running
    try:
        result = subprocess.run(['docker-compose', 'ps', 'ollama'], 
                              capture_output=True, text=True, check=True)
        if 'Up' not in result.stdout:
            click.echo("❌ Ollama service is not running. Start it first with: ai-dev-local start --ollama")
            sys.exit(1)
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to check Ollama status")
        sys.exit(1)
    
    # Get models to pull
    if models:
        model_list = models.split(',')
    else:
        import os
        model_list = os.getenv('OLLAMA_AUTO_PULL_MODELS', 'llama2:7b,codellama:7b,mistral:7b,phi:2.7b').split(',')
    
    click.echo(f"📥 Pulling models: {', '.join(model_list)}")
    
    for model in model_list:
        model = model.strip()
        click.echo(f"  • Pulling {model}...")
        try:
            subprocess.run(['docker-compose', 'exec', 'ollama', 'ollama', 'pull', model], 
                         check=True)
            click.echo(f"  ✅ Successfully pulled {model}")
        except subprocess.CalledProcessError:
            click.echo(f"  ❌ Failed to pull {model}")
    
    click.echo("🎉 Ollama initialization complete!")

@ollama.command()
def models():
    """List available Ollama models."""
    try:
        result = subprocess.run(['docker-compose', 'exec', 'ollama', 'ollama', 'list'], 
                              check=True)
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to list models. Make sure Ollama is running.", err=True)
        sys.exit(1)

@ollama.command()
@click.argument('model')
def pull(model):
    """Pull a specific Ollama model."""
    click.echo(f"📥 Pulling model: {model}")
    try:
        subprocess.run(['docker-compose', 'exec', 'ollama', 'ollama', 'pull', model], 
                     check=True)
        click.echo(f"✅ Successfully pulled {model}")
    except subprocess.CalledProcessError:
        click.echo(f"❌ Failed to pull {model}", err=True)
        sys.exit(1)

@ollama.command()
@click.argument('model')
def remove(model):
    """Remove a specific Ollama model."""
    click.echo(f"🗑️  Removing model: {model}")
    try:
        subprocess.run(['docker-compose', 'exec', 'ollama', 'ollama', 'rm', model], 
                     check=True)
        click.echo(f"✅ Successfully removed {model}")
    except subprocess.CalledProcessError:
        click.echo(f"❌ Failed to remove {model}", err=True)
        sys.exit(1)

@ollama.command('sync-litellm')
@click.option('--dry-run', is_flag=True, help='Show what would be changed without making modifications')
@click.option('--backup', is_flag=True, default=True, help='Create backup of existing config (default: true)')
def sync_litellm(dry_run, backup):
    """Sync LiteLLM configuration with currently available Ollama models."""
    import os
    import yaml
    import shutil
    from datetime import datetime
    
    click.echo("🔄 Syncing LiteLLM configuration with Ollama models...")
    
    # Check if Ollama service is running
    try:
        result = subprocess.run(['docker-compose', 'ps', 'ollama'], 
                              capture_output=True, text=True, check=True)
        if 'Up' not in result.stdout:
            click.echo("❌ Ollama service is not running. Start it first with: ai-dev-local start --ollama")
            sys.exit(1)
    except subprocess.CalledProcessError:
        click.echo("❌ Failed to check Ollama status")
        sys.exit(1)
    
    # Get currently installed Ollama models
    try:
        result = subprocess.run(['docker-compose', 'exec', '-T', 'ollama', 'ollama', 'list'], 
                              capture_output=True, text=True, check=True)
        ollama_output = result.stdout.strip()
        
        # Parse ollama list output to extract model names
        ollama_models = []
        for line in ollama_output.split('\n')[1:]:  # Skip header
            if line.strip():
                model_name = line.split()[0]  # First column is model name
                if ':' in model_name:
                    # Remove tag for LiteLLM compatibility, keep base name
                    base_name = model_name.split(':')[0]
                    ollama_models.append({'name': base_name, 'full_name': model_name})
                else:
                    ollama_models.append({'name': model_name, 'full_name': model_name})
        
        if not ollama_models:
            click.echo("⚠️  No Ollama models found. Run 'ai-dev-local ollama init' first.")
            return
        
        click.echo(f"📋 Found {len(ollama_models)} Ollama models: {', '.join(m['full_name'] for m in ollama_models)}")
        
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Failed to get Ollama models: {e}")
        sys.exit(1)
    
    # Read current LiteLLM config
    config_path = 'configs/litellm_config.yaml'
    if not os.path.exists(config_path):
        click.echo(f"❌ LiteLLM config file not found: {config_path}")
        sys.exit(1)
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        click.echo(f"❌ Failed to read LiteLLM config: {e}")
        sys.exit(1)
    
    # Create backup if requested and not dry run
    if backup and not dry_run:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{config_path}.backup_{timestamp}"
        try:
            shutil.copy2(config_path, backup_path)
            click.echo(f"💾 Created backup: {backup_path}")
        except Exception as e:
            click.echo(f"⚠️  Failed to create backup: {e}")
    
    # Find existing Ollama models in config
    existing_ollama_models = []
    other_models = []
    
    for model in config.get('model_list', []):
        if (model.get('litellm_params', {}).get('model', '').startswith('ollama/') or 
            'ollama' in model.get('litellm_params', {}).get('api_base', '')):
            existing_ollama_models.append(model)
        else:
            other_models.append(model)
    
    click.echo(f"🔍 Found {len(existing_ollama_models)} existing Ollama models in LiteLLM config")
    
    # Create new Ollama model configurations
    new_ollama_models = []
    for model in ollama_models:
        model_config = {
            'model_name': model['name'],
            'litellm_params': {
                'model': f"ollama/{model['full_name']}",
                'api_base': 'http://host.docker.internal:11434'
            }
        }
        new_ollama_models.append(model_config)
    
    # Update config with new Ollama models
    updated_config = config.copy()
    updated_config['model_list'] = other_models + new_ollama_models
    
    # Show changes
    click.echo("\n📊 Configuration Changes:")
    click.echo("=" * 50)
    
    if existing_ollama_models:
        click.echo(f"➖ Removing {len(existing_ollama_models)} old Ollama models:")
        for model in existing_ollama_models:
            click.echo(f"   • {model.get('model_name', 'unnamed')}")
    
    click.echo(f"➕ Adding {len(new_ollama_models)} current Ollama models:")
    for model in new_ollama_models:
        click.echo(f"   • {model['model_name']} -> {model['litellm_params']['model']}")
    
    # Update router settings if they exist
    if 'router_settings' in updated_config and 'model_group_alias' in updated_config['router_settings']:
        # Add ollama-group if there are ollama models
        if new_ollama_models:
            ollama_group = [m['model_name'] for m in new_ollama_models]
            updated_config['router_settings']['model_group_alias']['ollama-group'] = ollama_group
            click.echo(f"🔗 Updated ollama-group alias with {len(ollama_group)} models")
    
    if dry_run:
        click.echo("\n🔍 DRY RUN - No changes made")
        click.echo("Run without --dry-run to apply changes")
        return
    
    # Write updated config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(updated_config, f, default_flow_style=False, sort_keys=False, indent=2)
        
        click.echo(f"\n✅ Successfully updated {config_path}")
        click.echo(f"📋 Total models in config: {len(updated_config['model_list'])}")
        click.echo(f"   • Ollama models: {len(new_ollama_models)}")
        click.echo(f"   • Other models: {len(other_models)}")
        
        # Suggest restarting LiteLLM
        click.echo("\n💡 Restart LiteLLM to apply changes:")
        click.echo("   docker-compose restart litellm")
        
    except Exception as e:
        click.echo(f"❌ Failed to write updated config: {e}")
        sys.exit(1)

@ollama.command('list-available')
@click.option('--search', '-s', help='Search for models containing this term')
@click.option('--category', '-c', type=click.Choice(['all', 'popular', 'code', 'embedding', 'vision']), default='popular', help='Filter by model category')
@click.option('--format', '-f', type=click.Choice(['table', 'list', 'json']), default='table', help='Output format')
def list_available(search, category, format):
    """List all available models from Ollama library."""
    import json
    import requests
    from urllib.parse import urlencode
    
    click.echo("🔍 Fetching available Ollama models from library...")
    
    try:
        # Note: Ollama library API endpoint may not be publicly available
        # We'll use a fallback approach with static model data
        click.echo("📊 Using curated model list (registry API unavailable)")
        
        # Curated list of available Ollama models with metadata
        all_models = [
            {'name': 'llama2:7b', 'description': 'Meta Llama 2 7B - General purpose model', 'pulls': 1000000, 'tags': ['7b', 'latest']},
            {'name': 'llama2:13b', 'description': 'Meta Llama 2 13B - Larger general purpose model', 'pulls': 800000, 'tags': ['13b']},
            {'name': 'llama2:70b', 'description': 'Meta Llama 2 70B - Largest general purpose model', 'pulls': 500000, 'tags': ['70b']},
            {'name': 'llama3:8b', 'description': 'Meta Llama 3 8B - Latest generation model', 'pulls': 900000, 'tags': ['8b', 'latest']},
            {'name': 'llama3:70b', 'description': 'Meta Llama 3 70B - Latest large model', 'pulls': 600000, 'tags': ['70b']},
            {'name': 'codellama:7b', 'description': 'Code Llama 7B - Code generation model', 'pulls': 700000, 'tags': ['7b', 'code']},
            {'name': 'codellama:13b', 'description': 'Code Llama 13B - Larger code model', 'pulls': 500000, 'tags': ['13b', 'code']},
            {'name': 'codellama:34b', 'description': 'Code Llama 34B - Large code model', 'pulls': 300000, 'tags': ['34b', 'code']},
            {'name': 'mistral:7b', 'description': 'Mistral 7B - Fast and efficient model', 'pulls': 800000, 'tags': ['7b', 'instruct']},
            {'name': 'mistral:instruct', 'description': 'Mistral 7B Instruct - Instruction tuned', 'pulls': 600000, 'tags': ['instruct']},
            {'name': 'phi:2.7b', 'description': 'Microsoft Phi 2.7B - Small but capable', 'pulls': 400000, 'tags': ['2.7b']},
            {'name': 'phi3:3.8b', 'description': 'Microsoft Phi 3 3.8B - Latest small model', 'pulls': 350000, 'tags': ['3.8b']},
            {'name': 'gemma:2b', 'description': 'Google Gemma 2B - Ultra lightweight', 'pulls': 300000, 'tags': ['2b']},
            {'name': 'gemma:7b', 'description': 'Google Gemma 7B - Lightweight model', 'pulls': 450000, 'tags': ['7b']},
            {'name': 'qwen:7b', 'description': 'Alibaba Qwen 7B - Multilingual model', 'pulls': 250000, 'tags': ['7b', 'chat']},
            {'name': 'qwen:14b', 'description': 'Alibaba Qwen 14B - Larger multilingual', 'pulls': 180000, 'tags': ['14b', 'chat']},
            {'name': 'llava:7b', 'description': 'LLaVA 7B - Vision and language model', 'pulls': 200000, 'tags': ['7b', 'vision']},
            {'name': 'llava:13b', 'description': 'LLaVA 13B - Larger vision model', 'pulls': 150000, 'tags': ['13b', 'vision']},
            {'name': 'moondream:1.8b', 'description': 'Moondream 1.8B - Compact vision model', 'pulls': 100000, 'tags': ['1.8b', 'vision']},
            {'name': 'bakllava:7b', 'description': 'BakLLaVA 7B - Alternative vision model', 'pulls': 80000, 'tags': ['7b', 'vision']},
            {'name': 'nomic-embed-text', 'description': 'Nomic Embed - Text embedding model', 'pulls': 300000, 'tags': ['embedding']},
            {'name': 'mxbai-embed-large', 'description': 'MixedBread AI - Large embedding model', 'pulls': 150000, 'tags': ['embedding', 'large']},
            {'name': 'all-minilm:l6-v2', 'description': 'All MiniLM - Sentence embedding', 'pulls': 200000, 'tags': ['embedding', 'sentence']},
            {'name': 'codegemma:2b', 'description': 'Google CodeGemma 2B - Code model', 'pulls': 120000, 'tags': ['2b', 'code']},
            {'name': 'codegemma:7b', 'description': 'Google CodeGemma 7B - Larger code model', 'pulls': 100000, 'tags': ['7b', 'code']},
            {'name': 'starcoder:1b', 'description': 'StarCoder 1B - Compact code model', 'pulls': 90000, 'tags': ['1b', 'code']},
            {'name': 'starcoder:3b', 'description': 'StarCoder 3B - Medium code model', 'pulls': 80000, 'tags': ['3b', 'code']},
            {'name': 'deepseek-coder:1.3b', 'description': 'DeepSeek Coder 1.3B - Efficient code model', 'pulls': 70000, 'tags': ['1.3b', 'code']},
            {'name': 'deepseek-coder:6.7b', 'description': 'DeepSeek Coder 6.7B - Larger code model', 'pulls': 60000, 'tags': ['6.7b', 'code']}
        ]
        
        models = all_models
        
        # Filter by search term if provided
        if search:
            search_lower = search.lower()
            models = [m for m in models if search_lower in m['name'].lower() or search_lower in m['description'].lower()]
        
        # Filter by category
        if category != 'all':
            category_filters = {
                'popular': ['llama2', 'llama3', 'codellama', 'mistral', 'phi', 'gemma', 'qwen'],
                'code': ['codellama', 'codegemma', 'starcoder', 'wizard-coder', 'deepseek-coder'],
                'embedding': ['nomic-embed', 'mxbai-embed', 'all-minilm'],
                'vision': ['llava', 'moondream', 'bakllava']
            }
            
            if category in category_filters:
                filter_terms = category_filters[category]
                models = [m for m in models if any(term in m['name'].lower() for term in filter_terms)]
        
        if not models:
            click.echo(f"❌ No models found for category '{category}'" + (f" matching '{search}'" if search else ""))
            return
        
        # Sort by popularity (downloads or stars if available)
        models.sort(key=lambda x: x.get('pulls', 0), reverse=True)
        
        if format == 'json':
            click.echo(json.dumps(models, indent=2))
        elif format == 'list':
            click.echo(f"\n📋 Available models ({len(models)} found):")
            for model in models:
                name = model.get('name', 'Unknown')
                description = model.get('description', 'No description')
                click.echo(f"  • {name}: {description}")
        else:  # table format
            click.echo(f"\n📋 Available Ollama Models ({len(models)} found):")
            click.echo("=" * 80)
            click.echo(f"{'Name':<20} {'Tags':<15} {'Pulls':<10} {'Description'}")
            click.echo("-" * 80)
            
            for model in models[:50]:  # Limit to top 50 for readability
                name = model.get('name', 'Unknown')[:18]
                tags = ', '.join(model.get('tags', [])[:2])[:13]  # Show first 2 tags
                pulls = str(model.get('pulls', 0))
                if len(pulls) > 8:
                    pulls = f"{int(pulls)//1000}k"
                description = model.get('description', 'No description')[:35]
                
                click.echo(f"{name:<20} {tags:<15} {pulls:<10} {description}")
            
            if len(models) > 50:
                click.echo(f"\n... and {len(models) - 50} more models")
        
        click.echo(f"\n💡 Use 'ai-dev-local ollama pull <model-name>' to download a model")
        click.echo("💡 Use --search to filter models by name")
        click.echo("💡 Use --category to filter by type: popular, code, embedding, vision")
        
    except requests.RequestException as e:
        click.echo(f"❌ Failed to fetch models from Ollama library: {e}", err=True)
        click.echo("\n🔄 Fallback: Showing common models you can pull:")
        
        # Fallback list of popular models
        fallback_models = [
            ('llama2:7b', 'Meta Llama 2 7B - General purpose model'),
            ('llama2:13b', 'Meta Llama 2 13B - Larger general purpose model'),
            ('codellama:7b', 'Code Llama 7B - Code generation model'),
            ('mistral:7b', 'Mistral 7B - Fast and efficient model'),
            ('phi:2.7b', 'Microsoft Phi 2.7B - Small but capable model'),
            ('gemma:7b', 'Google Gemma 7B - Lightweight model from Google'),
            ('qwen:7b', 'Alibaba Qwen 7B - Multilingual model'),
            ('llava:7b', 'LLaVA 7B - Vision and language model'),
            ('nomic-embed-text', 'Nomic Embed - Text embedding model'),
            ('all-minilm:l6-v2', 'All MiniLM - Sentence embedding model')
        ]
        
        click.echo("\n📋 Popular Models:")
        click.echo("-" * 60)
        for name, description in fallback_models:
            click.echo(f"  • {name:<20} {description}")
    
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
