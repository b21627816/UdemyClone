from decimal import Decimal
from django.shortcuts import render
import os
from rest_framework.views import APIView
import json
from users.models import User
from courses.models import Course
from .models import PaymentIntent, Payment
from rest_framework import status
from rest_framework.response import Response
import stripe
from rest_framework.permissions import IsAuthenticated

# Create your views here.

stripe_api_key = os.environ.get('STRIPE_API_KEY')
endpoint_secret = ""  # Replace with your Stripe webhook endpoint secret

stripe.api_key = stripe_api_key


class PaymentHandler(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.body:
            body = json.loads(request.body)
            if body and len(body):
                course_line_items = []
                cart_courses = []
                for item in body:
                    try:
                        course = Course.objects.get(course_uuid=item)
                        line_item = {
                            "price_data": {
                                "currency": "usd",
                                "unit_amount": int(course.price * 100),
                                "product_data": {
                                    "name": course.title,
                                },
                            },
                            "quantity": 1,
                        }
                        course_line_items.append(line_item)
                        cart_courses.append(course)

                    except Course.DoesNotExist:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=course_line_items,
            mode="payment",
            success_url="http://localhost:3000/",
            cancel_url="http://localhost:3000/",
        )

        intent = PaymentIntent.objects.create(
            payment_intent_id=checkout_session.payment_intent,
            checkout_id=checkout_session.id,
            user=request.User.objects.get(id=1),
        )

        intent.courses.add(*cart_courses)

        return Response({"url": checkout_session.url})


class Webhook(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if event["type"] == "checkout.session.complete":
            session = event["data"]["object"]

            try:
                intent = PaymentIntent.objects.get(
                    checkout_id=session.id, payment_intent_id=session.payment_intent)
            except PaymentIntent.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            Payment.objects.create(
                payment_intent=intent,
                total_amount=Decimal(session.amount_total / 100),
            )

            intent.user.paid_courses.add(*intent.courses.all())

            return Response(status=status.HTTP_200_OK)
