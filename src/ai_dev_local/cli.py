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
        click.echo("  • Dashboard: http://localhost:3002")
        click.echo("  • Langfuse: http://localhost:3000")
        click.echo("  • FlowiseAI: http://localhost:3001")
        click.echo("  • Open WebUI: http://localhost:8081")
        click.echo("  • LiteLLM Proxy: http://localhost:4000")
        click.echo("  • Documentation: http://localhost:8000")
        if ollama:
            click.echo("  • Ollama: http://localhost:11434")
        
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
    
    click.echo("📚 Opening documentation...")
    webbrowser.open('http://localhost:8000')

@cli.command()
def dashboard():
    """Open dashboard in browser."""
    import webbrowser
    
    click.echo("🎛️ Opening dashboard...")
    webbrowser.open('http://localhost:3002')

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

if __name__ == '__main__':
    cli()
