from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.url import URL, URLCreate, URLResponse
from app.utils.helpers import generate_short_id
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
def shorten_url(url_in: URLCreate, db: Session = Depends(get_db)):
    # If custom_id is provided, check if it's already taken
    if url_in.custom_id:
        try:
            existing_custom = db.query(URL).filter(URL.short_id == url_in.custom_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Database error during custom ID validation")
        if existing_custom:
            # If same URL, just return the existing entry
            if existing_custom.original_url == str(url_in.original_url):
                return existing_custom
            raise HTTPException(status_code=400, detail="Custom ID already taken by another URL")
        short_id = url_in.custom_id
    else:
        # Check if URL already exists
        db_url = db.query(URL).filter(URL.original_url == str(url_in.original_url)).first()
        if db_url:
            return db_url
        
        short_id = generate_short_id()
        # Ensure generated short_id is unique
        while db.query(URL).filter(URL.short_id == short_id).first():
            short_id = generate_short_id()
            
    try:
        new_url = URL(original_url=str(url_in.original_url), short_id=short_id)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return new_url
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while shortening: {str(e)}"
        )

@router.get("/{short_id}")
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):
    # Ignore common browser requests that aren't short IDs
    if short_id in ["favicon.ico", "robots.txt", "sitemap.xml"]:
        raise HTTPException(status_code=404)
        
    db_url = db.query(URL).filter(URL.short_id == short_id).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Increment clicks
    try:
        db_url.clicks += 1
        db.commit()
    except Exception:
        db.rollback()
        # Still redirect even if click count update fails
        pass
    
    return RedirectResponse(url=db_url.original_url, status_code=status.HTTP_302_FOUND)

@router.get("/stats/{short_id}", response_model=URLResponse)
def get_url_stats(short_id: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_id == short_id).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url
