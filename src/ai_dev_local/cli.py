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
        git_tag = 'v0.2.0'
    
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
            'keys': ['GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'TIMEZONE', 'GITHUB_PERSONAL_ACCESS_TOKEN',
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

if __name__ == '__main__':
    cli()
