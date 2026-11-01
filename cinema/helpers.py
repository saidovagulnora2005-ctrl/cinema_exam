from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_email(booking):
    session = booking.session
    seat = booking.seat
    message = f"""
    Здравствуйте!

    Ваш билет успешно забронирован!

    Фильм: {session.movie.title}
    Зал: {session.hall.name}

    Ряд: {seat.row}
    Место: {seat.number}

    Дата: {session.start_time.strftime('%d.%m.%Y')}
    Время: {session.start_time.strftime('%H:%M')}

    Цена: {session.price} TJS

    Код подтверждения: {booking.confirmation_code}

    Оплата производится в кассе кинотеатра.

    Спасибо за выбор нашего кинотеатра!
    """
    
    send_mail(
        subject="Подтверждение бронирования — SG Cinema",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.email]
    )