from django.shortcuts import render, redirect
from .models import Theater, Screening, Booking, Seat
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    theaters = Theater.objects.all()
    return render(request, 'booking/index.html', {'theaters': theaters})

def reservation(request, theater_id):
    theater = Theater.objects.get(pk=theater_id)
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        seats = request.POST.getlist('seats')  # 여러 좌석 선택을 위해 getlist() 사용
        screening = Screening.objects.create(theater=theater, date=date, time=time)
        for seat_number in seats:
            Seat.objects.create(screening=screening, seat_number=seat_number, status=1)
        return HttpResponseRedirect(reverse('booking:booking_detail', args=(screening.id,)))
    return render(request, 'booking/reservation.html', {'theater': theater})

def booking_detail(request, screening_id):
    seats = Seat.objects.filter(screening_id=screening_id, status=1)
    return render(request, 'booking/booking_detail.html', {'seats': seats})

def theater_list(request):
    theaters = Theater.objects.all()
    return render(request, 'booking/theater_list.html', {'theaters': theaters})

def create_booking(request):
    if request.method == 'POST':
        screening_id = request.POST['screening_id']
        phone_number = request.POST['phone_number']

        screening = Screening.objects.get(pk=screening_id)
        theater = Theater.objects.get(pk=screening.theater_id)

        # 예약된 좌석들을 가져옵니다.
        booked_seats = Booking.objects.filter(screening=screening).values_list('seat_number', flat=True)

        # 상영관의 총 좌석 수
        total_seats = 10  # 총 좌석 수를 직접 설정합니다.

        if len(booked_seats) >= total_seats:
            # 좌석이 꽉 찼을 경우 예약 불가능한 메시지를 표시합니다.
            message = "모든 좌석이 예약되어 더 이상 예약이 불가능합니다."
            return render(request, 'booking/create_booking.html', {'screenings': Screening.objects.all(), 'message': message})

        # 빈 좌석을 찾아서 좌석 번호를 자동으로 부여합니다.
        seat_number = None
        for i in range(1, total_seats + 1):
            if i not in booked_seats:
                seat_number = i
                break

        booking = Booking(screening=screening, seat_number=seat_number, phone_number=phone_number)
        booking.save()

        success_message = f"예약이 완료되었습니다. 상영작: {theater.theater_name}, 일시: {screening.date}, {screening.time}, 좌석 번호: {seat_number}"
        return render(request, 'booking/create_booking.html', {'screenings': Screening.objects.all(), 'message': success_message})
        

    screenings = Screening.objects.all()
    context = {'screenings': screenings}
    return render(request, 'booking/create_booking.html', context)

def check_booking(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        bookings = Booking.objects.filter(phone_number=phone_number)
        booking_info = []

        for booking in bookings:
            screening = booking.screening
            theater_name = screening.theater.theater_name
            date_time = f"{screening.date}, {screening.time}"
            booking_info.append((theater_name, date_time, booking.seat_number))

        if not booking_info:
            message = "예매 내역이 없습니다."
            return render(request, 'booking/check_booking.html', {'message': message})
        

        return render(request, 'booking/check_booking.html', {'booking_info': booking_info})
    
    return render(request, 'booking/check_booking.html')
