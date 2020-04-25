
class PositionPiece:
    def __init__(self, id_pos_sc=None, id_pos_paroi=None, link_paroi=None, link_volume=None, type_piece=None):
        # Initialisation des variables
        self._id_pos_sc = id_pos_sc             # id position piece dans le pare douche (sc)
        self._id_pos_paroi = id_pos_paroi       # id position piece dans la paroi
        self._link_paroi = link_paroi           # Link between paroi
        self._link_volume = link_volume         # Link between volume
        self._pieces = []                       # Vecteur piece
        self._type = type_piece                 # Type de piece
        self._connection_between_volume = 1     #

    # Add piece
    # def add_piece(self):
    #     self._pieces.append(Piece(link=self._link_paroi, connection_type=self._connection_between_volume))

    def _get_pieces(self):
        return self._pieces

    def _get_link(self):
        return self._link_paroi

    def _set_link(self, link):
        self._link_paroi = link

    def _get_connection(self):
        return self._connection_between_volume

    def _set_connection(self, connection):
        self._connection_between_volume = connection
        # for i in range(len(self._pieces)):
        #     self._pieces[i].connection = connection
        #     self._pieces[i].define_connection()

    def _get_type(self):
        return self._type

    def _get_id_pos_sc(self):
        return self._id_pos_sc

    def _get_id_pos_paroi(self):
        return self._id_pos_paroi

    def _set_id_pos_paroi(self, id):
        self._id_pos_paroi = id

    pieces = property(_get_pieces)
    link = property(_get_link, _set_link)
    connection = property(_get_connection, _set_connection)
    type = property(_get_type)
    id_pos_sc = property(_get_id_pos_sc)
    id_pos_paroi = property(_get_id_pos_paroi, _set_id_pos_paroi)