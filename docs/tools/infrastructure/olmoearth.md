# OLMoEarth

OLMoEarth is an open geospatial foundation model platform and distributed processing infrastructure developed by the Allen Institute for AI (Ai2), designed for planet-scale satellite data analysis and environmental modeling.

## What it is

OLMoEarth is an end-to-end platform for Earth observation, geospatial modeling, and continent-scale inference. Built on Ai2's extensive history with open models (such as OLMo) and geospatial platforms (like EarthRanger and Skylight), the OLMoEarth family of foundation models is pre-trained on roughly 10 terabytes of multimodal satellite data. The accompanying OLMoEarth Platform provides the required high-performance distributed infrastructure to label data, fine-tune models, find/access satellite imagery from multiple providers, and perform large-scale inference cost-effectively.

## What problem it solves

While governments and environmental NGOs require AI to monitor deforestation, food security, and wildfire risks, most do not have the specialized ML infrastructure teams needed to manage raw geospatial pipelines. Geospatial data is notoriously complex: satellite images are scattered across multiple providers, use different projections and resolutions, and total dozens of terabytes.

OLMoEarth solves this by providing a robust, fault-tolerant execution platform. It handles projections alignment, resolution adjustments, and geographic consistency stitching, recovering automatically from routine node failures in distributed environments.

## Where it fits in the stack

**Infrastructure / Geospatial Processing Layer**. S sits above cloud imagery directories (like Google Earth Engine or AWS Sentinel) and below high-level visualization and analytical tools, performing raw tensor operations and spatial maps generation.

```
┌────────────────────────────────────────┐
│      Application / Visualization       │
│         (EarthRanger, Skylight)        │
└───────────────────┬────────────────────┘
                    │ Geospatial Queries & Alert Triggers
┌───────────────────▼────────────────────┐
│          OLMOEARTH PLATFORM            │
└───────────────────┬────────────────────┘
                    │ Scale Distributed Inference / Geo-Stitching
┌───────────────────▼────────────────────┐
│ Multimodal Satellite Providers (AWS/GEE)│
└────────────────────────────────────────┘
```

## Typical use cases

- **Deforestation Monitoring**: Tracking tree cover changes over continent-scale areas with rapid inference passes.
- **Wildfire Risk Forecasting**: Utilizing thermal and environmental sensors to generate real-time local hazard maps.
- **Agricultural Food Security**: Monitoring crop health, field yields, and soil hydration states across regional borders.
- **Ocean and Maritime Safety**: Correlating sat-data to identify illegal fishing fleets or oil spill drift behaviors.

## Strengths

- **Pre-trained on 10TB of Satellite Data**: Native understanding of high-resolution, multi-channel Earth imagery.
- **Planet-Scale Infrastructure**: Capable of processing continent-scale regions in roughly a day, dealing with dozens of terabytes of imagery.
- **Highly Cost-Effective**: Optimizes processing pipelines, reducing computation costs down to fractions of a penny per square kilometer.
- **Fault-Tolerant Geo-Stitching**: Integrates automatic retry and recovery behaviors for distributed task runners.
- **Open Science Driven**: Follows Ai2's standard of open weights and open data access, fostering global scientific collaboration.

## Limitations

- **Infrastructure Heavy**: Running the full local distributed platform requires significant containerized clusters (Kubernetes) and deep storage connectivity.
- **Specialized Input Format**: Built specifically for satellite/geospatial multi-band rasters, not applicable to general-purpose business image recognition.

## When to use it

- When executing environmental monitoring pipelines that span large geographical regions or continuous historical timelines.
- When you want to run open-weight geospatial foundation models on custom, cost-effective infrastructure.
- In humanitarian, NGO, or municipal planning workloads needing actionable environmental insights.

## When not to use it

- For standard general-purpose computer vision tasks (like face detection, OCR, or object detection in common images).
- When a simple, small localized vision model (such as MageVL) is sufficient for narrow camera feeds.

## Getting started

The platform is accessible via Ai2's OlmoEarth repositories and geospatial APIs.

```bash
# Registering and downloading OlmoEarth models
pip install olmoearth-sdk
```

## CLI examples

```bash
# Run localized satellite tile inference for deforestation markers
olmoearth-cli run --model olmoearth-v1 --aoi brazil_sector_4.geojson --output deforestation_map.tiff

# Monitor active platform processing jobs
olmoearth-cli jobs list --status active
```

## API examples

### Geospatial Tile Pipeline Setup and Pydantic v2 Schema Validation
Processing satellite tiles requires strict coordinate, projection, and spectral-band validation before scheduling distributed tensor workloads. This Python example uses Pydantic v2 to validate an ingestion request payload.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

class SatelliteTileMetadata(BaseModel):
    tile_id: str = Field(description="Unique code identifying the Sentinel/Landsat tile")
    spectral_bands: List[str] = Field(..., min_items=3, description="List of bands, e.g., RED, GREEN, BLUE, NIR")
    projection: Literal["EPSG:4326", "EPSG:3857"] = Field(default="EPSG:4326")
    cloud_cover_percentage: float = Field(..., ge=0.0, le=100.0)
    bounding_box: List[float] = Field(..., description="[min_lon, min_lat, max_lon, max_lat]")

    @field_validator("bounding_box")
    @classmethod
    def validate_bbox(cls, v: List[float]) -> List[float]:
        if len(v) != 4:
            raise ValueError("Bounding box must contain exactly 4 coordinates [min_lon, min_lat, max_lon, max_lat]")
        if not (-180.0 <= v[0] <= 180.0) or not (-90.0 <= v[1] <= 90.0):
            raise ValueError("Coordinates are out of physical Earth boundaries.")
        return v

# Ingestion configuration payload
payload = {
    "tile_id": "T22HGA_20261123",
    "spectral_bands": ["RED", "GREEN", "BLUE", "NIR", "SWIR"],
    "projection": "EPSG:4326",
    "cloud_cover_percentage": 14.2,
    "bounding_box": [-47.8825, -15.7942, -47.8525, -15.7642]
}

# Validate tile parameters using Pydantic v2
validated_tile = SatelliteTileMetadata(**payload)

print(f"Validated OLMoEarth Tile config: {validated_tile.tile_id}")
print(f"Cloud Cover: {validated_tile.cloud_cover_percentage}% - Suitable for processing.")
```

## Related tools / concepts

- [MageVL](../frameworks/magevl.md) — For localized streaming video analysis at the edge.
- [Kubernetes (K3s)](../infrastructure/k3s.md) — The lightweight orchestrator frequently used to manage local GIS container instances.
- [Docker](../infrastructure/docker.md) — Base container system for scaling tile processing nodes.
- [MinIO](../intake_storage/minio.md) — S3-compatible local storage for raw geospatial satellite raster files.

## Sources / references

- [The OlmoEarth Platform Blog - Allen Institute for AI](https://allenai.org/blog/olmoearth-infrastructure)
- [Official OLMoEarth Platform Web App](https://olmoearth.allenai.org/)

## Contribution Metadata

- Last reviewed: 2026-11-23
- Confidence: high
