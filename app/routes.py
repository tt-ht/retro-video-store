
import re
from marshmallow import schema
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort

from datetime import date 
import datetime, requests, os

from dotenv import load_dotenv

load_dotenv()


video_bp = Blueprint("videos", __name__, url_prefix="/videos")
from app.models.video import PutVideoInputSchema
put_video_schema = PutVideoInputSchema()

@video_bp.route("", methods=["POST"])
def create_video():
    request_data=request.get_json()
    # not_field=put_video_schema.validate(request.form)
    if "title" not in request_data: 
        invalid_data={"details": "Request body must include title."}
        return jsonify(invalid_data),400
    elif "release_date" not in request_data:
        invalid_data={"details": "Request body must include release_date."}
        return jsonify(invalid_data),400
    elif "total_inventory" not in request_data:
        invalid_data={"details": "Request body must include total_inventory."}
        return jsonify(invalid_data),400
    
    new_video=Video(title=request_data["title"], release_date=request_data["release_date"], total_inventory=request_data["total_inventory"])
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201

@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos_response = []
    videos = Video.query.all()
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response), 200



@video_bp.route("/<id>", methods=["GET"])
def get_one_video(id):
    id=validate_id_int(id)
    video = Video.query.get(id)
    if not video:
        return {"message":f"Video {id} was not found"}, 404
    # if request.method=="GET":
    return jsonify({"title": video.title, "id": video.id, "total_inventory": video.total_inventory}), 200
    

@video_bp.route("/<id>", methods=["PUT"])
def put_one_video(id): 
    id=validate_id_int(id)
    video = Video.query.get(id)
    if not video:
        return {"message":f"Video {id} was not found"}, 404   
    request_data=request.get_json()
    errors = put_video_schema.validate(request_data)
    if errors:
    # if "title" not in request_data: 
    #     invalid_data={"details": "Request body must include title."}
    #     return jsonify(invalid_data),400
    # elif "release_date" not in request_data:
    #     invalid_data={"details": "Request body must include release_date."}
    #     return jsonify(invalid_data),400
    # elif "total_inventory" not in request_data:
    #     invalid_data={"details": "Request body must include total_inventory."}
    #     return jsonify(invalid_data),400
        return jsonify({"details": f"{errors} Invalid data"}),400
    else:
        video.title=request_data["title"]
        video.release_date=request_data["release_date"]
        video.total_inventory=request_data["total_inventory"]
        db.session.commit()
        return jsonify(video.to_dict()),200

@video_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    id=validate_id_int(id)
    
    video = Video.query.get(id)

    if video:
        db.session.delete(video)
        db.session.commit()
        return {"id": video.id}, 200
    else:
        return {"message":f"Video {id} was not found"}, 404

def validate_id_int(id):
    try:
        id = int(id)
        return (id)
    except:
        abort(400, "Error: id needs to be a number")


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# creates a customer
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return make_response(
            {"details": f"Request body must include name."}, 400
        )
    
    elif "postal_code" not in request_body:
        return make_response(
            {"details": f"Request body must include postal_code."}, 400
        )

    elif "phone" not in request_body:
        return make_response(
            {"details": f"Request body must include phone."}, 400
        )

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"]
    )

    new_customer.registered_at = datetime.datetime.now()

    db.session.add(new_customer)
    db.session.commit()

    return make_response(
        new_customer.to_dict(), 201
    )

# lists all existing customers and details about each customer
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers_response = []
    customers = Customer.query.all()

    for customer in customers:
        customers_response.append(customer.to_dict())
    return jsonify(customers_response), 200

# gets details about a specific customer
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400
        
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    return make_response(
        customer.to_dict(), 200
    )

# updates and return details about a specific customer
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400

    customer = Customer.query.get(customer_id)
    request_body = request.get_json()

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    if "name" not in request_body:
        return make_response(
            {"details": f"Request body must include name."}, 400
        )
    
    elif "postal_code" not in request_body:
        return make_response(
            {"details": f"Request body must include postal_code."}, 400
        )

    elif "phone" not in request_body:
        return make_response(
            {"details": f"Request body must include phone."}, 400
        )

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    return jsonify({
        "name": f"{customer.name}",
        "phone": f"{customer.phone}",
        "postal_code": f"{customer.postal_code}"
        }        
    )
    

# deletes a specific customer
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    if not customer_id.isnumeric():
        return { "error": f"{customer_id} must be numeric."}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    db.session.delete(customer)
    db.session.commit()

    return make_response(
        {"id": customer.id}, 200
    )

    # return {"id": customer.id}, 200

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# checks out a video to a customer, and updates the data in the database
    # request should:
    # create a rental for the specific video and customer
    # create a due date (7 days from current date)
    
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)

def create_check_out():
    request_body = request.get_json()
    
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    video=Video.query.get(request_body["video_id"])
    customer=Customer.query.get(request_body["customer_id"])

    # returns 404 error if missing customer, video, or no available inventory
    if customer is None or video is None:
        return jsonify({"details": "invalid data"}), 404

    # if the number of videos checked out == the video's total inventory, there are none left to check out
    if len(video.rentals) == video.total_inventory:
        return jsonify({"message": "Could not perform checkout"}), 400        

    new_rental = Rental(
        video_id = request_body["video_id"],
        customer_id = request_body["customer_id"]
    )
    
    db.session.add(new_rental)
    db.session.commit()
   
    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": len(customer.videos_rented),
        "available_inventory": video.total_inventory-len(video.rentals)
        }), 200

# checks in a video to a customer, and updates the data in the database as such
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in():
    request_body = request.get_json()
    
    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    video=Video.query.get(request_body["video_id"])
    customer=Customer.query.get(request_body["customer_id"])
    
    video_id = request_body["video_id"]
    customer_id = request_body["customer_id"]

    # returns 404 error if missing customer, video, or no available inventory
    if customer is None or video is None:
        return jsonify({"details": "invalid data"}), 404

    for rental in video.rentals: # every rental of the video currently checked out
        if rental.customer_id == customer_id:
            db.session.delete(rental)
            db.session.commit()
            return jsonify({
                "customer_id": customer_id,
                "video_id": video_id,
                "videos_checked_out_count": len(customer.videos_rented),
                "available_inventory": video.total_inventory-len(video.rentals)
                }), 200
        else:
            break
    return jsonify({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}), 400

# lists the videos a customer currently has checked out
# @customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
# def videos_checked_out_by_customer(customer_id):
#     customer = Customer.query.get(customer_id)

#     if customer is None:
#         return make_response(
#             {"message": f"Customer {customer_id} was not found"}, 404)

#     videos_checked_out = []

#     rentals = db.session.query(Rental).filter(Rental.customer_id==customer_id).all()   # every rental with the matching customer_id
#     for rental in rentals:
#         video = Video.query.get(rental.video_id)
#         videos_checked_out.append(
#             {
#                 "title": video.title,
#                 "release_date": video.release_date,
#                 "due_date": rental.due_date
#             }
#         )

#     return jsonify(videos_checked_out), 200

# lists the videos a customer currently has checked out
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def videos_checked_out_by_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(
            {"message": f"Customer {customer_id} was not found"}, 404)

    videos_checked_out = []

    rentals = customer.videos_rented   # every rental with the matching customer_id
    for rental in rentals:
        video = Rental.query.get(rental.id)
        videos_checked_out.append(
            {
                "title": video.title,
                "release_date": video.release_date,
                "due_date": rental.due_date
            }
        )

    return jsonify(videos_checked_out), 200

@video_bp.route("<video_id>/rentals", methods=["GET"])
def get_all_videos_rented(video_id):

    videos_rented=Video.renters
    for video in videos_rented:
        
    request_data=request.get_json()
    check_out_videos=[]
    rentals_of_video=Rental.query.filter_by(video_id)
    for video_id in rentals_of_video:
        check_out_videos.append(rentals_of_video)
    for one_video in check_out_videos:
        return jsonify({
            "due_date": one_video.due_date, 
            "customers":[one_video.customer_id.put_request_dict() for one_video in one_video.customer_rentals]}), 200


    return jsonify({"id": goal.goal_id, "title":goal.title, "tasks":[task.to_dict() for task in goal.tasks]}), 200

    