import pandas as pd
import numpy as np


class Volume:
    def __init__(self):
        # UI initialisation
        self._l_cst = -9999                 # fixe width of the volume
        self._cote = [150, 150, 300, 300]   # cote of the volume
        self._df_pieces = None              # data frame pieces
        self._df_jeu = None                 # data frame jeu (use for notch)
        self._button = []                   # vecteur bouton
        self._notch = []                    # vecteur encoches
        self._l_left_angle = 0
        self._h_left_angle = 0
        self._l_right_angle = 0
        self._h_right_angle = 0
        self._l_left_slope = 0
        self._h_left_slope = 0
        self._l_right_slope = 0
        self._h_right_slope = 0
        # Type de verre
        self._ep_verre = 8                  # Epaisseur du verre

        # Template of the volume
        self._matrix_template = np.array([[0, 0, 0, 0],
                                          [1, 0, 0, 0],
                                          [1, 0, 1, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 0]])

    def jeu_bas(self):
        """
        Return the clearance at the position 2. Use when the door add common notch with fixed glass
        """
        df = self._df_jeu
        jeu = df[df['POS_PIECE_PAROI'] % 3 == 2]['JEU']
        return float(jeu)

    def update_button(self):
        """
        Calculate the positions of the button
        """
        for button in self._button:
            button.calculate_pos_abs(l_verre=self._cote[0], h_verre=self._cote[2])
            button.calculate_pos_trou()

    def update_notch(self):
        """
        Calculate the positions of the notch
        """
        for notch in self._notch:
            notch.calculate_pos_rel(l_verre=self._cote[0] + self._l_left_angle + self._l_right_angle,
                                    h_verre=self._cote[2])
            notch.calculate_pos_abs(l_verre=self._cote[0] + self._l_left_angle + self._l_right_angle,
                                    h_verre=self._cote[2])

    def volume_point(self):
        """ Return the point of the polygon.
                Use with the dxf export"""
        r = 1
        cote = np.array([[self._cote[0] * r, 0],
                         [0 * r, 0],
                         [0, self._cote[2] * r],
                         [0, 0 * r]])
        points = np.dot(self._matrix_template, cote)
        return points

    def area(self):
        """ Return the area of the volume in m2 """
        largeur = self._cote[0]
        hauteur = self._cote[2]
        area = largeur * hauteur / 1000000
        return float(area)

    # GET and SET functions
    def _get_name(self):
        return self._name

    def _get_id_ref_verre(self):
        return self._id_ref_verre

    def _get_ep_verre(self):
        return self._ep_verre

    def _get_type(self):
        return self._type

    def _get_l_cst(self):
        return self._l_cst

    def _get_l_left_angle(self):
        return self._l_left_angle

    def _get_h_left_angle(self):
        return self._h_left_angle

    def _get_l_right_angle(self):
        return self._l_right_angle

    def _get_h_right_angle(self):
        return self._h_right_angle

    def _get_l_left_slope(self):
        return self._l_left_slope

    def _get_h_left_slope(self):
        return self._h_left_slope

    def _get_l_right_slope(self):
        return self._l_right_slope

    def _get_h_right_slope(self):
        return self._h_right_slope

    def _get_cote(self):
        return self._cote

    def _set_cote(self, value):
        self._cote = value

    def _get_df_pieces(self):
        return self._df_pieces

    def _set_df_pieces(self, value):
        self._df_pieces = value
        # Group by PAROI, TYPE_JEU, POS_PIECE summarise by SUM(JEU) to add jeu by positions
        self._df_jeu = pd.DataFrame(self._df_pieces.groupby(['PAROI', 'TYPE_JEU', 'POS_PIECE_PAROI'],
                                                            as_index=False)
                                    ['JEU'].sum())
        print(self._df_pieces)
        print(self.profil_length())

    def _get_df_jeu(self):
        return self._df_jeu

    def _get_button(self):
        return self._button

    def _get_notch(self):
        return self._notch

    name = property(_get_name)
    id_ref_verre = property(_get_id_ref_verre)
    ep_verre = property(_get_ep_verre)
    type = property(_get_type)
    l_cst = property(_get_l_cst)
    cote = property(_get_cote, _set_cote)
    df_pieces = property(_get_df_pieces, _set_df_pieces)
    df_jeu = property(_get_df_jeu)
    button = property(_get_button)
    notch = property(_get_notch)
    l_left_angle = property(_get_l_left_angle)
    h_left_angle = property(_get_h_left_angle)
    l_right_angle = property(_get_l_right_angle)
    h_right_angle = property(_get_h_right_angle)
    l_left_slope = property(_get_l_left_slope)
    h_left_slope = property(_get_h_left_slope)
    l_right_slope = property(_get_l_right_slope)
    h_right_slope = property(_get_h_right_slope)