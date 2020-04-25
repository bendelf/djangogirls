import numpy as np


class ParoiApp:
    def __init__(self, paroi):
        # Initialisation des variables
        self._id = paroi.id
        self._name = paroi.name         # Name of paroi
        self._h_finie = paroi.h_finie   # Hauteur finie
        self._l_finie = paroi.l_finie   # Largeur finie

        self._volume = []               # Contener volume

        # To calculate cote coupe --> c - t(t(a%*% sj))
        self._matrix = np.array([])     # a
        self._v_cote = np.zeros(0)      # c
        self._nv_lcst = 0               # Numbers of volume with width constant

    # Add volume in _volume
    def add_volume(self, volume):
        self._volume.append(volume)

    def create_matrix(self):
        nv = len(self._volume) - self._nv_lcst  # number of volume where the calcul will be effectuate
        m = np.zeros((len(self._volume) * 4, (len(self._volume) * 3) + 1))
        v = np.zeros(len(self._volume) * 3 + 1)
        v[np.arange(0, len(self._volume) * 3 + 1, 3)] = 1/nv

        for i in range(0, len(self._volume)):
            if self._volume[i].checkBoxLCst.isChecked() is True:
                m[i * 4: i * 4 + 2, :] = 0
            else:
                m[i * 4: i * 4 + 2, :] = v

            m[i * 4 + 2: i * 4 + 4, i * 3:(i + 1) * 3 + 1] = np.reshape([0, 1, 1, 0,
                                                                         0, 1, 1, 0],
                                                                        (2, 4))
        self._matrix = m

    def create_vector_cote(self):
        self._v_cote = np.zeros((len(self._volume) * 4))
        self._nv_lcst = 0  # initialisation à zero
        l_cst = 0  # sum of width constant cote

        for i in range(0, len(self._volume)):
            if self._volume[i].checkBoxLCst.isChecked() is True:
                l_cst += self._volume[i].l_cst
                self._nv_lcst += 1

        for i in range(0, len(self._volume)):
            if self._volume[i].checkBoxLCst.isChecked() is True:
                self._v_cote[i * 4] = self._volume[i].l_cst
                self._v_cote[i * 4 + 1] = self._volume[i].l_cst
            else:
                self._v_cote[i * 4] = (self._l_finie - l_cst) / (len(self._volume) - self._nv_lcst)
                self._v_cote[i * 4 + 1] = (self._l_finie - l_cst) / (len(self._volume) - self._nv_lcst)

            self._v_cote[i * 4 + 2] = self._h_finie
            self._v_cote[i * 4 + 3] = self._h_finie

    def _get_id(self):
        return self._id

    def _get_volumes(self):
        return self._volume

    def _get_l_finie(self):
        return self._l_finie

    def _set_l_finie(self, l_finie):
        self._l_finie = l_finie

    def _get_h_finie(self):
        return self._h_finie

    def _set_h_finie(self, h_finie):
        self._h_finie = h_finie

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = name

    l_finie = property(_get_l_finie, _set_l_finie)
    h_finie = property(_get_h_finie, _set_h_finie)
    id = property(_get_id)
    volumes = property(_get_volumes)
    name = property(_get_name, _set_name)