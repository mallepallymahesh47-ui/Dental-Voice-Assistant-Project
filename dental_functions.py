# Mongo db memory
from mongoDB import doctors_collection, appointments_collection
from datetime import datetime
from bson import ObjectId


APPOINTMENTS_DB = {"appointments": {}, "next_id": 1}

DENTISTS_DB = {
    "dr_smith": {
        "name": "Dr. John Smith",
        "specialization": "General Dentist",
        "available_slots": ["10:00 AM", "11:00 AM", "3:00 PM"]
    },
    "dr_emily": {
        "name": "Dr. Emily Davis",
        "specialization": "Orthodontist",
        "available_slots": ["9:00 AM", "1:00 PM", "4:00 PM"]
    },
    "dr_raj": {
        "name": "Dr. Raj Kumar",
        "specialization": "Oral Surgeon",
        "available_slots": ["12:00 PM", "2:00 PM", "5:00 PM"]
    }
}

SYMPTOM_ROUTER = {
    "tooth pain": "dr_smith",
    "braces": "dr_emily",
    "wisdom tooth": "dr_raj",

}


# Function

def find_doctor_by_name(doctor_name):
    for key, doctor in DENTISTS_DB.items():
        if doctor["name"].lower() == doctor_name.lower():
            return key, doctor
    return None, None


# Core Functions

def get_dentist_info(doctor_name):
    key, doctor = find_doctor_by_name(doctor_name)

    if doctor:
        return {
            "doctor_key": key,
            "name": doctor["name"],
            "specialization": doctor["specialization"],
            "available_slots": doctor["available_slots"]
        }

    return {"error": f"Dentist '{doctor_name}' not found"}


def recommend_dentist(symptom):
    doctor = doctors_collection.find_one({"doctor_key": "dr_smith"})

    if not doctor:
        return {"error": "No doctor found"}

    return {
        "name": doctor["name"],
        "specialization": doctor["specialization"],
        "available_slots": doctor["available_slots"]
    }



def book_appointment(patient_name, doctor_name, time_slot):
    doctor = doctors_collection.find_one({
        "name": {"$regex": f"^{doctor_name}$", "$options": "i"}
    })

    if not doctor:
        return {"error": f"Dentist '{doctor_name}' not found"}

    # slot locking
    result = doctors_collection.update_one(
        {
            "_id": doctor["_id"],
            "available_slots": time_slot
        },
        {
            "$pull": {"available_slots": time_slot}
        }
    )

    if result.modified_count == 0:
        return {"error": f"Slot '{time_slot}' not available"}

    appointment = {
        "patient": patient_name,
        "doctor": doctor["name"],
        "time": time_slot,
        "status": "confirmed",
        "created_at": datetime.utcnow()
    }

    inserted = appointments_collection.insert_one(appointment)

    return {
        "appointment_id": str(inserted.inserted_id),
        "message": f"Appointment confirmed with {doctor['name']} at {time_slot}"
    }




def lookup_appointment(appointment_id):
    appointment = appointments_collection.find_one(
        {"_id": ObjectId(appointment_id)}
    )

    if not appointment:
        return {"error": "Appointment not found"}

    return {
        "patient": appointment["patient"],
        "doctor": appointment["doctor"],
        "time": appointment["time"],
        "status": appointment["status"]
    }


def cancel_appointment(appointment_id):
    appointment = APPOINTMENTS_DB["appointments"].get(int(appointment_id))

    if not appointment:
        return {"error": f"Appointment {appointment_id} not found"}

    appointment["status"] = "cancelled"

    return {
        "appointment_id": appointment_id,
        "message": "Appointment cancelled successfully"
    }


# Function Map

FUNCTION_MAP = {
    "get_dentist_info": get_dentist_info,
    "recommend_dentist": recommend_dentist,
    "book_appointment": book_appointment,
    "lookup_appointment": lookup_appointment,
    "cancel_appointment": cancel_appointment
}

