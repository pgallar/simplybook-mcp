import logging
import sys
import os
import asyncio
from typing import Dict, Any
from fastmcp import FastMCP
from simplybook.auth.routes import AuthRoutes
from simplybook.bookings.routes import BookingsRoutes
from simplybook.clients.routes import ClientsRoutes
from simplybook.services.routes import ServicesRoutes
from simplybook.providers.routes import ProvidersRoutes
from simplybook.statistics.routes import StatisticsRoutes
from simplybook.tickets.routes import TicketsRoutes
from simplybook.memberships.routes import MembershipsRoutes
from simplybook.coupons.routes import CouponsRoutes
from simplybook.notes.routes import NotesRoutes
from simplybook.products.routes import ProductsRoutes
from simplybook.subscription.routes import SubscriptionRoutes
from simplybook.payments.routes import PaymentsRoutes
from simplybook.exceptions import SimplyBookException

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('simplybook_mcp.log')
        ]
    )

def get_credentials() -> tuple:
    """Obtener credenciales desde variables de entorno"""
    company = os.getenv('SIMPLYBOOK_COMPANY')
    login = os.getenv('SIMPLYBOOK_LOGIN')
    password = os.getenv('SIMPLYBOOK_PASSWORD')
    
    if not company or not login or not password:
        raise ValueError("SIMPLYBOOK_COMPANY, SIMPLYBOOK_LOGIN y SIMPLYBOOK_PASSWORD environment variables are required")
    
    return company, login, password

def create_mcp_server() -> FastMCP:
    try:
        mcp = FastMCP("simplybook")
        return mcp
    except Exception as e:
        logging.getLogger(__name__).critical(f"Failed to create MCP server: {str(e)}")
        raise

def register_routers(mcp: FastMCP, company: str, login: str, password: str) -> None:
    logger = logging.getLogger(__name__)
    routers = [
        AuthRoutes(),
        BookingsRoutes(company, login, password),
        ClientsRoutes(company, login, password),
        ServicesRoutes(company, login, password),
        ProvidersRoutes(company, login, password),
        StatisticsRoutes(company, login, password),
        TicketsRoutes(company, login, password),
        MembershipsRoutes(company, login, password),
        CouponsRoutes(company, login, password),
        NotesRoutes(company, login, password),
        ProductsRoutes(company, login, password),
        SubscriptionRoutes(company, login, password),
        PaymentsRoutes(company, login, password)
    ]

    for router in routers:
        try:
            router.register_tools(mcp)
            logger.debug(f"Registered router: {router.__class__.__name__}")
        except Exception as e:
            logger.error(f"Failed to register router {router.__class__.__name__}: {str(e)}")
            raise

def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Initializing SimplyBook MCP server...")
        
        # Obtener credenciales
        company, login, password = get_credentials()
        logger.info("Credentials loaded successfully")
        
        mcp = create_mcp_server()
        
        logger.info("Registering routers...")
        register_routers(mcp, company, login, password)
        logger.info("All routers registered successfully")
        
        logger.info("Starting SimplyBook MCP server on port 8000...")
        import asyncio
        
        async def run_server():
            await mcp.run_async(transport="http", host="0.0.0.0", port=8000)
        
        asyncio.run(run_server())
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()