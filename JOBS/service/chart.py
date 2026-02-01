from fastapi import FastAPI,APIRouter,Depends
from sqlalchemy.orm import Session
from ..Database import get_db
import matplotlib.pyplot as plt
from io import BytesIO



#router = APIRouter()

#@router.get("/dashboard/chart")
#async def dashboard_chart(db:Session=Depends(get_db)):
#    data = get_dashboard_data(db)
#    fig = generate_dashboard_chart(data)
#    buf = BytesIO()
#    fig.savefig(buf,format='png')
#    buf.seek(0)
#    return StreamingResponse(buf, media_type="image/png")



def generate_dashboard_chart(data):
    """
    data = [
        {"title": "Software Engineer", "views": 120, "applications": 15},
        {"title": "Data Analyst", "views": 90, "applications": 25},
        ...
    ]
    """
    titles = [d["title"] for d in data]
    views = [d["views"] for d in data]
    applications = [d["applications"] for d in data]
    conversion = [(a/v*100 if v > 0 else 0) for a,v in zip(applications, views)]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    # Bar chart for views and applications
    ax1.bar(titles, views, label="Views", alpha=0.7)
    ax1.bar(titles, applications, label="Applications", alpha=0.7)
    ax1.set_ylabel("Counts")
    ax1.legend(loc="upper left")

    # Line chart for conversion rate
    ax2 = ax1.twinx()
    ax2.plot(titles, conversion, color="green", marker="o", label="Conversion Rate (%)")
    ax2.set_ylabel("Conversion Rate (%)")
    ax2.legend(loc="upper right")

    plt.title("Job Views vs Applications with Conversion Rate",fontsize=16,fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save chart to memory buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

