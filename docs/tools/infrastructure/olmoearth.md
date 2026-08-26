# OLMoEarth

OLMoEarth is an open geospatial foundation model platform and distributed processing infrastructure developed by the Allen Institute for AI (Ai2), designed for planet-scale satellite data analysis, climate monitoring, and environmental modeling.

## What it is

OLMoEarth is an end-to-end platform for Earth observation, geospatial foundation modeling, and continent-scale inference. Built on Ai2's open model ecosystem (including the OLMo 2 series) and geospatial platforms (such as EarthRanger and Skylight), the OLMoEarth 2.0 family of geospatial foundation models is pre-trained on tens of terabytes of multimodal satellite, SAR, and climate data. The accompanying OLMoEarth Platform provides high-performance distributed infrastructure to ingest imagery, fine-tune models, access satellite feeds across public/private providers, and perform large-scale inference cost-effectively.

## What problem it solves

While governments, humanitarian agencies, and environmental NGOs require AI to monitor deforestation, agricultural security, and disaster risks, most lack dedicated ML infrastructure teams to manage raw geospatial pipelines. Geospatial data is exceptionally complex: satellite images span multiple spectral bands, SAR radar modes, dynamic resolutions, and varying projections across petabytes of files.

OLMoEarth solves this by providing a resilient, fault-tolerant execution platform. It handles projections alignment, spatial resolution resampling, dynamic temporal stitching, and automatically recovers from node failures in distributed GPU environments.

## Where it fits in the stack

**Infrastructure / Geospatial Processing Layer**. Sits above cloud satellite image registries (such as AWS Sentinel, Google Earth Engine, and Planetary Computer) and below analytical dashboards, executing vision-language-spatial operations and generating actionable GIS layers.

```
┌────────────────────────────────────────┐
│      Application / Visualization       │
│         (EarthRanger, Skylight)        │
└───────────────────┬────────────────────┘
                    │ Spatial Queries & FastMCP 3.1 Alerts
┌───────────────────▼────────────────────┐
│          OLMOEARTH PLATFORM            │
└───────────────────┬────────────────────┘
                    │ Distributed GPU Inference / Geo-Stitching
┌───────────────────▼────────────────────┐
│ Multimodal Satellite Registries (AWS/GEE)│
└────────────────────────────────────────┘
```

## Typical use cases

- **Deforestation & Land-Use Monitoring**: Tracking illegal logging and canopy coverage changes across continent-scale biomes with sub-meter spatial accuracy.
- **Wildfire Risk Forecasting**: Combining thermal, SAR, and vegetation health metrics to generate predictive local fire propagation maps.
- **Agricultural Security**: Monitoring crop health, drought indexes, and soil moisture across multi-national agricultural regions.
- **Maritime Safety & Surveillance**: Correlating synthetic aperture radar (SAR) and optical feeds to identify unauthorized vessels or ocean spill hazards.
- **Agentic Geospatial Workflows**: Integrating with FastMCP 3.1 tool servers to allow agentic systems (driven by Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra) to run spatial queries programmatically.

## Strengths

- **Pre-trained Multimodal Geospatial Models**: Native support for optical, multispectral, and SAR satellite rasters.
- **Planet-Scale Infrastructure**: Processes continent-scale territories efficiently using distributed cloud-native worker nodes.
- **Cost-Optimized Execution**: Pipeline optimization reduces compute cost to fractions of a cent per square kilometer.
- **Fault-Tolerant Geo-Stitching**: Automated recovery for distributed tile processing and temporal series alignment.
- **Open Science Commitment**: Adheres to Ai2's standard of open model weights, training datasets, and benchmarks (comparing favorably with IBM/NASA Prithvi and AlphaEarth).

## Limitations

- **Infrastructure Heavy**: Deploying the full self-hosted platform requires Kubernetes clusters with high-bandwidth S3/object storage access.
- **Domain Specific**: Optimized strictly for spatial rasters and remote sensing data, not general-purpose business image classification.

## When to use it

- When executing environmental monitoring pipelines that span large geographical regions or continuous historical timelines.
- When building agentic RAG or automated alert systems that require programmatic geospatial spatial analysis.
- In humanitarian, municipal planning, or climate action workloads requiring open-weights foundation models.

## When not to use it

- For standard computer vision tasks (such as document OCR or facial recognition).
- When simple localized video analytics (such as [MageVL](../frameworks/magevl.md)) on edge cameras are sufficient.

## Getting started

The platform is accessible via Ai2's OLMoEarth SDK and geospatial endpoints:

```bash
# Registering and downloading OLMoEarth SDK
pip install olmoearth-sdk FastMCP pydantic
```

## CLI examples

```bash
# Run localized satellite tile inference for deforestation markers
olmoearth-cli run --model olmoearth-v2 --aoi brazil_sector_4.geojson --output deforestation_map.tiff

# Monitor active platform processing jobs
olmoearth-cli jobs list --status active
```

## API examples

### Geospatial Tile Pipeline Setup and Pydantic v2 Schema Validation
Processing satellite tiles requires strict coordinate, projection, and spectral-band validation before scheduling distributed tensor workloads under FastMCP 3.1 environments. This Python example uses Pydantic v2 to validate an ingestion request payload.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal

class SatelliteTileMetadata(BaseModel):
    tile_id: str = Field(description="Unique code identifying the Sentinel/Landsat/SAR tile")
    spectral_bands: List[str] = Field(..., min_items=3, description="List of bands, e.g., RED, GREEN, BLUE, NIR, SAR_VV")
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
    "tile_id": "T22HGA_20270107",
    "spectral_bands": ["RED", "GREEN", "BLUE", "NIR", "SWIR", "SAR_VV"],
    "projection": "EPSG:4326",
    "cloud_cover_percentage": 8.4,
    "bounding_box": [-47.8825, -15.7942, -47.8525, -15.7642]
}

# Validate tile parameters using Pydantic v2
validated_tile = SatelliteTileMetadata(**payload)

print(f"Validated OLMoEarth Tile config: {validated_tile.tile_id}")
print(f"Cloud Cover: {validated_tile.cloud_cover_percentage}% - Suitable for processing.")
```

## Related tools / concepts

- [MageVL](../frameworks/magevl.md) — For localized streaming video analysis at the edge.
- [K3s](k3s.md) — Lightweight orchestrator used to manage containerized GIS worker instances.
- [Docker](docker.md) — Container framework for scaling tile processing nodes.
- [MinIO](../intake_storage/minio.md) — S3-compatible local storage for satellite rasters.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard protocol for agentic tool integration.

## Sources / references

- [The OLMoEarth Platform Blog - Allen Institute for AI](https://allenai.org/blog/olmoearth-infrastructure)
- [Official OLMoEarth Platform Web App](https://olmoearth.allenai.org/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
