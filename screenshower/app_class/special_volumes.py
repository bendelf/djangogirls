from screenshower.app_class.fixe import Fixe
import numpy as np
import pandas as pd


class Special(Fixe):
    def __init__(self, volume=None):
        self._name = volume.name
        self._type = 11
        self._l_cst = volume.l_cste
        self._l_left_angle = volume.l_left_angle
        self._h_left_angle = volume.h_left_angle
        self._l_right_angle = volume.l_right_angle
        self._h_right_angle = volume.h_right_angle
        self._l_left_slope = volume.l_left_slope
        self._h_left_slope = volume.h_left_slope
        self._l_right_slope = volume.l_right_slope
        self._h_right_slope = volume.h_right_slope


        # Template of the volume
        self._matrix_template = np.array([[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                          [1, 1, 1, 0, -1, 0, 0, 0, 0, 0],
                                          [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                                          [1, 1, 1, 0, 0, 1, 0, -1, 0, 0],
                                          [1, 1, 0, 0, 0, 1, 0, -1, 0, 0],
                                          [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                          [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                                          [0, 1, 0, 0, 0, 1, -1, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 1, -1, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]])

    def volume_point(self):
        """ Return the point of the polygon.
                Use with the dxf export"""
        r = 1
        cote = np.array([[self._cote[0] * r, 0],
                          [self._l_left_angle * r, 0],
                          [self._l_right_angle * r, 0],
                          [self._l_left_slope * r, 0],
                          [self._l_right_slope * r, 0],
                          [0, self._cote[2] * r],
                          [0, self._h_left_angle * r],
                          [0, self._h_right_angle * r],
                          [0, self._h_left_slope * r],
                          [0, self._h_right_slope * r]])
        points = np.dot(self._matrix_template, cote)

        return points

    @staticmethod
    def cote_point(pts):
        """ Return the point to draw the dimensions"""

        point = [(QPointF(pts[9, 0] * RATIO_V, pts[0, 1] * RATIO_V - 50),
                  QPointF(pts[0, 0] * RATIO_V, pts[0, 1] * RATIO_V - 50)),
                 (QPointF(pts[0, 0] * RATIO_V, pts[0, 1] * RATIO_V - 50),
                  QPointF(pts[1, 0] * RATIO_V, pts[1, 1] * RATIO_V - 50)),
                 (QPointF(pts[1, 0] * RATIO_V, pts[1, 1] * RATIO_V - 50),
                  QPointF(pts[2, 0] * RATIO_V, pts[1, 1] * RATIO_V - 50)),

                 (QPointF(pts[2, 0] * RATIO_V + 50, pts[1, 1] * RATIO_V),
                  QPointF(pts[2, 0] * RATIO_V + 50, pts[2, 1] * RATIO_V)),
                 (QPointF(pts[2, 0] * RATIO_V + 50, pts[2, 1] * RATIO_V),
                  QPointF(pts[3, 0] * RATIO_V + 50, pts[3, 1] * RATIO_V)),
                 (QPointF(pts[3, 0] * RATIO_V + 50, pts[3, 1] * RATIO_V),
                  QPointF(pts[3, 0] * RATIO_V + 50, pts[5, 1] * RATIO_V)),

                 (QPointF(pts[3, 0] * RATIO_V, pts[5, 1] * RATIO_V + 50),
                  QPointF(pts[5, 0] * RATIO_V, pts[5, 1] * RATIO_V + 50)),
                 (QPointF(pts[5, 0] * RATIO_V, pts[5, 1] * RATIO_V + 50),
                  QPointF(pts[6, 0] * RATIO_V, pts[6, 1] * RATIO_V + 50)),
                 (QPointF(pts[6, 0] * RATIO_V, pts[6, 1] * RATIO_V + 50),
                  QPointF(pts[8, 0] * RATIO_V, pts[6, 1] * RATIO_V + 50)),

                 (QPointF(pts[8, 0] * RATIO_V - 50, pts[6, 1] * RATIO_V),
                  QPointF(pts[8, 0] * RATIO_V - 50, pts[8, 1] * RATIO_V)),
                 (QPointF(pts[8, 0] * RATIO_V - 50, pts[8, 1] * RATIO_V),
                  QPointF(pts[9, 0] * RATIO_V - 50, pts[9, 1] * RATIO_V)),
                 (QPointF(pts[9, 0] * RATIO_V - 50, pts[9, 1] * RATIO_V),
                  QPointF(pts[9, 0] * RATIO_V - 50, pts[0, 1] * RATIO_V))]

        return point

    def update_slope_size(self):
        """
        Update the height and width of the slope with the running clearance
        """
        df = self._df_jeu
        print(df)
        self.accept_volume()  # on recupère à chaque run la valeur dans la fenêtre
        if self._l_left_slope > 0:
            self._l_left_slope -= float(df[df['POS_PIECE_PAROI'] % 4 == 1]['JEU'])

        if self._l_right_slope > 0:
            self._l_right_slope -= float(df[df['POS_PIECE_PAROI'] % 4 == 0]['JEU'])

        if self._h_left_slope > 0:
            self._h_left_slope -= float(df[df['POS_PIECE_PAROI'] % 3 == 0]['JEU'])

        if self._h_right_slope > 0:
            self._h_right_slope -= float(df[df['POS_PIECE_PAROI'] % 3 == 0]['JEU'])

    def _get_df_pieces(self):
        return self._df_pieces

    def _set_df_pieces(self, value):
        """
        Re implemented to update slope size
        """
        self._df_pieces = value
        # Group by PAROI, TYPE_JEU, POS_PIECE summarise by SUM(JEU) to add jeu by positions
        self._df_jeu = pd.DataFrame(self._df_pieces.groupby(['PAROI', 'TYPE_JEU', 'POS_PIECE_PAROI'],
                                                            as_index=False)
                                    ['JEU'].sum())
        self.update_slope_size()

    df_pieces = property(_get_df_pieces, _set_df_pieces)




