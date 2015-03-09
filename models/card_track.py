import sqlalchemy as sa
from transport.models.bus_track import BusTrack
from transport.models.map_point import MapPoint


class CardTrack(object):

    metadata = sa.MetaData()

    STATUS_NEW = 0
    STATUS_DRIVE = 1
    STATUS_END = 3

    OUT_DATED = 60 * 60 * 3  # 3 hour

    KEYS = ['cardid', 'carddata', 'blockid', 'lat', 'lon', 'time']

    MESSAGE_FROM_HOME = u'Ваш ребенок сел в автобус около дома'
    MESSAGE_TO_HOME = u'Ваш ребенок доставлен на автобусе домой'
    MESSAGE_FROM_SCHOOL = u'Ваш ребенок сел в автобус около школы'
    MESSAGE_TO_SCHOOL = u'Ваш ребенок доставлен на автобусе в школу'

    table = sa.Table(
        'bus_track',
        metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('blockid', sa.String(128), nullable=False),
        sa.Column('carddata', sa.String(128), nullable=False),
        sa.Column('blockid', sa.String(128), nullable=False),
        sa.Column('time', sa.Integer, nullable=False),
        sa.Column('lat', sa.Float, nullable=False),
        sa.Column('lon', sa.Float, nullable=False),
        sa.Column('status', sa.Integer, default=STATUS_NEW),
        sa.Column('start_point', sa.Integer),
    )

    def get_message(self, point_type, event_type):
        answer = False

        if self.STATUS_NEW == self.status and BusTrack.TYPE_START == event_type:
            if MapPoint.TYPE_SCHOOL == point_type:
                answer = self.MESSAGE_FROM_SCHOOL
            elif MapPoint.TYPE_HOME == point_type:
                answer = self.MESSAGE_FROM_HOME
        elif self.STATUS_DRIVE == self.status and BusTrack.TYPE_STOP == event_type:
            if MapPoint.TYPE_SCHOOL == point_type:
                answer = self.MESSAGE_TO_SCHOOL
            elif MapPoint.TYPE_HOME == point_type:
                answer = self.MESSAGE_TO_HOME

        return answer
