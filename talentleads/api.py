from ninja import NinjaAPI
from blog.api import router as blog_router

api = NinjaAPI(
    title="TalentLeads API",
    version="1.0.0",
    description="API for TalentLeads platform",
)

# Add blog router
api.add_router("/blog", blog_router)
