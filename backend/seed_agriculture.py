from backend.database import SessionLocal
from backend.models.farm import Farm


def seed_farms():
    db = SessionLocal()

    try:
        existing_farms = db.query(Farm).count()

        if existing_farms > 0:
            print("Farms already exist. Skipping seed.")
            return

        farms = [
            Farm(
                name="Eastern Cape Smallholder Farm",
                location="Eastern Cape",
                address="Eastern Cape, South Africa",
                latitude=-32.2968,
                longitude=26.9149,
                farm_size_hectares=12.5,
                soil_type="Loam",
                water_availability="Limited"
            ),

            Farm(
                name="Cape Town Community Farm",
                location="Khayelitsha, Cape Town",
                address="Khayelitsha, Cape Town, Western Cape",
                latitude=-34.0407,
                longitude=18.6770,
                farm_size_hectares=4.5,
                soil_type="Sandy Loam",
                water_availability="Moderate"
            ),

            Farm(
                name="Cape Winelands Farm",
                location="Stellenbosch",
                address="Stellenbosch, Western Cape",
                latitude=-33.9321,
                longitude=18.8602,
                farm_size_hectares=35.0,
                soil_type="Clay Loam",
                water_availability="Good"
            )
        ]

        db.add_all(farms)
        db.commit()

        print("Agriculture farms seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding farms: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_farms()