from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import ValidationError
from typing import List
from sqlalchemy.orm import Session

from src.models.domain.data_source import DataSource
from src.models.dtos.data_source_dto import DataSourceDTO
from src.utils.database import get_session


router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@router.post("/", response_model=DataSource, status_code=status.HTTP_201_CREATED)
async def create_data_source(
    payload: DataSourceDTO, db: Session = Depends(get_session)
):
    """
    Create a new data source.

    Args:
    - data_source: A `DataSource` Schema object containing the data source details.

    Returns:
    - The created `DataSource` object.
    """
    try:
        data_source = DataSource.model_schema(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        db.add(data_source)
        db.commit()
        db.refresh(data_source)
    return payload


@router.get("/", response_model=List[DataSource])
async def get_all_data_sources():
    """
    Get all data sources.

    Returns:
    - A list of `DataSource` objects.
    """
    try:
        return []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_source(name: str):
    """
    Delete a data source.

    Args:
    - name: The name of the data source.
    """
    try:
        # Add data source deletion logic here (e.g., database deletion)
        # For demonstration purposes, we'll just pass
        pass
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
