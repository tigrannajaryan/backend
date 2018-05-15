import datetime

import pytest
import pytz

from django_dynamic_fixture import G
from psycopg2.extras import DateRange

from api.v1.stylist.serializers import (
    StylistAvailableWeekDaySerializer,
    StylistProfileStatusSerializer,
    StylistSerializer,
    StylistServiceSerializer,
)
from core.choices import USER_ROLE
from core.models import User
from salon.models import (
    Salon,
    ServiceCategory,
    ServiceTemplate,
    Stylist,
    StylistAvailableWeekDay,
    StylistDateRangeDiscount,
    StylistService,
    StylistWeekdayDiscount,
)


@pytest.fixture
def stylist_data() -> Stylist:
    salon = G(
        Salon,
        name='Test salon', address='2000 Rilma Lane', city='Los Altos', state='CA',
        zip_code='94022', latitude=37.4009997, longitude=-122.1185007
    )

    stylist_user = G(
        User,
        is_staff=False, is_superuser=False, email='test_stylist@example.com',
        first_name='Fred', last_name='McBob', phone='(650) 350-1111',
        role=USER_ROLE.stylist,
    )
    stylist = G(
        Stylist,
        salon=salon, user=stylist_user,
        work_start_at=datetime.time(8, 0), work_end_at=datetime.time(15, 0),
    )

    return stylist


class TestStylistSerializer(object):
    @pytest.mark.django_db
    def test_stylist_serializer_representation(self, stylist_data: Stylist):
        serializer = StylistSerializer(instance=stylist_data)
        data = serializer.data
        assert(data['first_name'] == 'Fred' and data['last_name'] == 'McBob')
        assert(data['salon_name'] == 'Test salon')
        assert(data['id'] == stylist_data.id)

    @pytest.mark.django_db
    def test_stylist_serializer_update(self, stylist_data: Stylist):
        data = {
            'first_name': 'Jane',
            'last_name': 'McBob',
            'phone': '(650) 350-1111',
            'salon_name': 'Janes beauty',
            'salon_address': '1234 Front Street',
            # TODO: uncomment below lines when we enable address splitting
            # 'salon_city': 'Menlo Park',
            # 'salon_zipcode': '12345',
            # 'salon_state': 'CA',
        }
        serializer = StylistSerializer(
            instance=stylist_data, data=data, context={'user': stylist_data.user}
        )
        serializer.is_valid(raise_exception=True)
        stylist = serializer.save()
        assert(stylist.user.first_name == 'Jane')
        assert(stylist.salon.name == 'Janes beauty')

    @pytest.mark.django_db
    def test_stylist_create(self):
        user: User = G(
            User,
            email='stylist@example.com',
            role=USER_ROLE.stylist,
        )
        assert(user.is_stylist() is True)
        data = {
            'first_name': 'Jane',
            'last_name': 'McBob',
            'phone': '(650) 350-1111',
            'salon_name': 'Test salon',
            'salon_address': '1234 Front Street',
            # TODO: uncomment below lines when we enable address splitting
            # 'salon_city': 'Menlo Park',
            # 'salon_zipcode': '12345',
            # 'salon_state': 'CA',
        }
        serializer = StylistSerializer(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        stylist: Stylist = serializer.save()
        assert(stylist is not None)
        assert(stylist.user.id == user.id)
        assert(stylist.salon.name == 'Test salon')
        assert(stylist.salon.timezone == pytz.timezone('America/New_York'))
        assert(stylist.user.first_name == 'Jane')
        assert(stylist.available_days.count() == 7)


class TestStylistServiceSerializer(object):
    @pytest.mark.django_db
    def test_create(self):
        stylist: Stylist = G(Stylist)
        category: ServiceCategory = G(ServiceCategory)
        template: ServiceTemplate = G(
            ServiceTemplate,
            duration=datetime.timedelta(),
            name='service 1', category=category,
        )
        data = [
            {
                'name': 'service 1',
                'duration_minutes': 10,
                'base_price': 20,
                'is_enabled': True,
                'category_uuid': category.uuid
            }
        ]
        serializer = StylistServiceSerializer(
            data=data,
            context={'stylist': stylist},
            many=True
        )
        assert(serializer.is_valid(raise_exception=True))

        serializer.save()
        assert(StylistService.objects.count() == 1)
        service = StylistService.objects.last()
        assert(service.name == 'service 1')
        assert(service.duration == datetime.timedelta(minutes=10))
        assert(service.base_price == 20)
        assert(service.service_uuid == template.uuid)

    @pytest.mark.django_db
    def test_update(self):
        stylist = G(Stylist)
        category: ServiceCategory = G(ServiceCategory)
        stylist_service = G(
            StylistService,
            stylist=stylist,
            category=category,
            name='old name',
            duration=datetime.timedelta(0),
            base_price=10,
            is_enabled=True,
            deleted_at=None
        )
        old_service_uuid = stylist_service.service_uuid
        data = [
            {
                'id': stylist_service.id,
                'name': 'new name',
                'duration_minutes': 10,
                'base_price': 20,
                'is_enabled': True,
                'category_uuid': category.uuid
            }
        ]
        serializer = StylistServiceSerializer(
            data=data,
            context={'stylist': stylist},
            many=True
        )
        assert (serializer.is_valid(raise_exception=True))

        serializer.save()
        assert (StylistService.objects.count() == 1)
        service = StylistService.objects.last()
        assert (service.name == 'new name')
        assert (service.duration == datetime.timedelta(minutes=10))
        assert (service.base_price == 20)
        assert(old_service_uuid != service.service_uuid)


class TestStylistProfileCompletenessSerializer(object):
    @pytest.mark.django_db
    def test_completed_profile(self, stylist_data: Stylist):
        user = stylist_data.user
        assert(
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_personal_data'] is True
        )
        user.first_name = ''
        user.last_name = ''
        user.phone = ''
        user.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_personal_data'] is False
        )
        user.phone = '12345'
        user.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_personal_data'] is False
        )
        user.first_name = 'Fred'
        user.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_personal_data'] is True
        )
        salon = stylist_data.salon
        salon.address = ''
        salon.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_personal_data'] is False
        )

    @pytest.mark.django_db
    def test_profile_picture(self, stylist_data: Stylist):
        user = stylist_data.user
        user.photo = None
        user.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_picture_set'] is False
        )
        user.photo = 'http://example.com/1.jpg'
        user.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_picture_set'] is True
        )

    @pytest.mark.django_db
    def test_services_set(self, stylist_data: Stylist):
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_services_set'] is False
        )
        G(StylistService, stylist=stylist_data, duration=datetime.timedelta(0))
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_services_set'] is True
        )

    @pytest.mark.django_db
    def test_business_hours_set(self, stylist_data: Stylist):
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_business_hours_set'] is False
        )
        G(StylistAvailableWeekDay, weekday=1, stylist=stylist_data, is_available=False)
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_business_hours_set'] is False
        )
        G(StylistAvailableWeekDay, weekday=2, stylist=stylist_data, is_available=True,
          work_start_at=datetime.time(8, 0), work_end_at=datetime.time(15, 0))
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_business_hours_set'] is True
        )

    @pytest.mark.django_db
    def test_weekday_discounts_set(self, stylist_data: Stylist):
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_weekday_discounts_set'] is False
        )
        G(StylistWeekdayDiscount, stylist=stylist_data)
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_weekday_discounts_set'] is True
        )

    @pytest.mark.django_db
    def test_other_discounts_set(self, stylist_data: Stylist):
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_other_discounts_set'] is False
        )
        stylist_data.first_time_book_discount_percent = 10
        stylist_data.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_other_discounts_set'] is True
        )
        stylist_data.first_time_book_discount_percent = 0
        stylist_data.rebook_within_1_week_discount_percent = 10
        stylist_data.save()
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_other_discounts_set'] is True
        )
        stylist_data.first_time_book_discount_percent = 0
        stylist_data.rebook_within_1_week_discount_percent = 0
        stylist_data.save()
        G(
            StylistDateRangeDiscount, stylist=stylist_data,
            dates=DateRange(datetime.date(2018, 4, 8), datetime.date(2018, 4, 10))
        )
        assert (
            StylistProfileStatusSerializer(
                instance=stylist_data).data['has_other_discounts_set'] is True
        )


class TestStylistAvailableWeekDaySerializer(object):

    @pytest.mark.django_db
    def test_create(self):
        stylist = G(Stylist)
        data = {
            'weekday_iso': 1,
            'is_available': True,
            'work_start_at': '8:00',
            'work_end_at': '15:30'
        }
        serializer = StylistAvailableWeekDaySerializer(
            data=data, context={'user': stylist.user}
        )
        assert(serializer.is_valid(raise_exception=False))
        available_day = serializer.save()
        assert(available_day.work_start_at == datetime.time(8, 0))
        assert(available_day.work_end_at == datetime.time(15, 30))
        assert(available_day.stylist == stylist)
        assert(available_day.is_available is True)

    @pytest.mark.django_db
    def test_validate(self):
        stylist = G(Stylist)
        data = {
            'weekday_iso': 1,
            'is_available': False,
        }
        serializer = StylistAvailableWeekDaySerializer(
            data=data, context={'user': stylist.user}
        )
        assert(serializer.is_valid(raise_exception=False) is True)

        data['is_available'] = True
        serializer = StylistAvailableWeekDaySerializer(
            data=data, context={'user': stylist.user}
        )
        assert (serializer.is_valid(raise_exception=False) is False)

        data['work_start_at'] = '8:00'
        serializer = StylistAvailableWeekDaySerializer(
            data=data, context={'user': stylist.user}
        )
        assert (serializer.is_valid(raise_exception=False) is False)

        data['work_end_at'] = '15:30'
        serializer = StylistAvailableWeekDaySerializer(
            data=data, context={'user': stylist.user}
        )
        assert (serializer.is_valid(raise_exception=False) is True)
