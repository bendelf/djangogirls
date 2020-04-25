from screenshower.app_class.position_piece import PositionPiece
from screenshower.app_class.paroi_app import ParoiApp
from screenshower.app_class.fixe import Fixe
from screenshower.app_class.porte import Porte
from screenshower.app_class.special_volumes import Special

import pandas as pd


class ScreenShower:
    def __init__(self, closed=0):
        self._position_pieces = []
        self._closed = closed
        self._paroi = []
        self._current_paroi = 0

    def load_paroi(self, parois):
        for paroi in parois:
            self._paroi.append(ParoiApp(paroi=paroi))

    @staticmethod
    def load_volume(paroi, volumes):

        for volume in volumes:
            if volume.type == 10:
                paroi.add_volume(Fixe(name=volume.name))
            if volume.type == 20:
                paroi.add_volume(Porte(name=volume.name))
            if volume.type == 11:
                paroi.add_volume(Special(name=volume.name))

    def load_piece(self):
        print('toto')

    def generate_position_pieces(self, parois):
        """
        Generate piece position
        """
        self._position_pieces = []

        for i in range(0, len(parois)):
            for j in range(0, len(parois[i].volumes)):
                if i == 0 and j == 0:
                    for k in range(0, 3):
                        if k == 0:
                            self._position_pieces.append(PositionPiece(
                                id_pos_sc=len(self._position_pieces) + 1,
                                id_pos_paroi=[(j * 3) + 1],
                                link_paroi=[parois[i]], type_piece='LATERAL'))
                        else:
                            self._position_pieces.append(PositionPiece(
                                id_pos_sc=len(self._position_pieces) + 1,
                                id_pos_paroi=[(j * 3) + k + 1],
                                link_paroi=[parois[i]], type_piece='VERTICAL'))
                else:
                    for k in range(0, 2):
                        self._position_pieces.append(PositionPiece(
                            id_pos_sc=len(self._position_pieces) + 1,
                            id_pos_paroi=[j * 3 + k + 2],
                            link_paroi=[parois[i]], type_piece='VERTICAL'))

                if i < len(parois) - 1 and j == len(parois[i].volumes) - 1:
                    self._position_pieces.append(PositionPiece(
                        id_pos_sc=len(self._position_pieces) + 1,
                        id_pos_paroi=[(j * 3) + 4, 1],
                        link_paroi=[parois[i], parois[i + 1]],
                        type_piece='LATERAL'))
                else:
                    if self.checkBoxClosed.isChecked() is not True or j < len(parois[i].volumes) - 1:
                        self._position_pieces.append(PositionPiece(
                            id_pos_sc=len(self._position_pieces) + 1,
                            id_pos_paroi=[(j * 3) + 4],
                            link_paroi=[parois[i]], type_piece='LATERAL'))
                    # if link_paroi P1 and Pn --> pare douche bouclé
                    else:
                        self._position_pieces[0].link = [parois[0], parois[i]]
                        self._position_pieces[0].id_pos_paroi = [1, (j * 3) + 4]

    def create_df_jeu(self):
        """
        Creation du data.frame jeu suivant le lien des pièces avec la paroi
        """
        # TODO : voir quand une seule piece sur la position et qu'elle n'est pas liée au 2 parois --> bug

        df_jeu = pd.DataFrame(index=None, columns=['PAROI', 'POS_PIECE_SC', 'POS_PIECE_PAROI', 'TYPE_JEU', 'REF_PIECE',
                                                   'JEU_REPORT', 'JEU', 'LINK'])

        for i in range(0, len(self._position_pieces)):
            if len(self._position_pieces[i].pieces) == 0:
                # Si pas de pieces dans la position ---> jeu = 0 par défaut
                for k in range(0, len(self._position_pieces[i].link)):
                    df_jeu = df_jeu.append({'PAROI': self._position_pieces[i].link[k].name,
                                            'POS_PIECE_SC': self._position_pieces[i].id_pos_sc,
                                            'POS_PIECE_PAROI': self._position_pieces[i].id_pos_paroi[k],
                                            'TYPE_JEU': self._position_pieces[i].type,
                                            'TYPE_PIECE': -9999,
                                            'REF_PIECE': 'Aucun jeu défini',
                                            'JEU_REPORT': 0,
                                            'JEU': 0},
                                           ignore_index=True)
            else:
                for j in range(0, len(self._position_pieces[i].pieces)):
                    for k in range(0, len(self._position_pieces[i].pieces[j].link)):
                        if self._position_pieces[i].pieces[j].link_report_piece[k] == 0:
                            df_jeu = df_jeu.append({'PAROI': self._position_pieces[i].link[k].name,
                                                    'POS_PIECE_SC': self._position_pieces[i].id_pos_sc,
                                                    'POS_PIECE_PAROI': self._position_pieces[i].id_pos_paroi[k],
                                                    'TYPE_JEU': self._position_pieces[i].type,
                                                    'TYPE_PIECE': -9999,
                                                    'REF_PIECE': 'Aucun jeu défini',
                                                    'JEU_REPORT': 0,
                                                    'JEU': 0},
                                                   ignore_index=True)
                        else:
                            df_jeu = df_jeu.append(
                                {'PAROI': self._position_pieces[i].pieces[j].link[k].name,
                                 'POS_PIECE_SC': self._position_pieces[i].id_pos_sc,
                                 'POS_PIECE_PAROI': self._position_pieces[i].id_pos_paroi[k],
                                 'TYPE_JEU': self._position_pieces[i].type,
                                 'TYPE_PIECE': self._position_pieces[i].pieces[j].type_piece,
                                 'REF_PIECE': self._position_pieces[i].pieces[j].ref,
                                 'JEU_REPORT': self._position_pieces[i].pieces[j].link_report_jeu[k],
                                 'JEU': self._position_pieces[i].pieces[j].jeu_report[k]},
                                ignore_index=True)

        # Attribute jeu for each PAROI
        for paroi in self._paroi:
            df_filter_paroi = df_jeu[df_jeu["PAROI"] == paroi.name]
            paroi.df_pieces = df_filter_paroi.sort_values(by=['POS_PIECE_PAROI'])

        return df_jeu

    def _get_parois(self):
        return self._paroi

    def _get_position_pieces(self):
        return self._position_pieces

    parois = property(_get_parois)
    position_pieces = property(_get_position_pieces)





