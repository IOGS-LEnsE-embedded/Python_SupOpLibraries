import usb.core
import usb.util
from utilities import *
from erle import encode


class dmd():
    """Classe permettant de contrôler la puce DLP6500 du DMD de 
    Texas Instruments par USB.

    Pour que le programme puisse établir une communication avec la puce, 
    il est nécessaire d'installer le pilote libusb-win32 
    (https://sourceforge.net/projects/libusb-win32/) correspondant.

    Remarque : Pour le DLP6500, les identifiants USB sont toujours 
    idVendor=0x0451 et idProduct=0xc900

    Ce programme se base sur le code écrit par Paolo Pozzi
    (https://github.com/csi-dcsc/Pycrafter6500).

    Vocabulaire :
        - pattern : un pattern est défini comme une image et ses paramètres 
        (temps d'exposition, temps de pause ou dark time, profondeur de bit, 
        couleur etc.) Voir fonction dmd.define_pattern().

        - séquence : suite de patterns.
    """

    def __init__(self):
        self.device = usb.core.find(idVendor=0x0451, idProduct=0xc900)
        self.device.set_configuration()

    def command(self,
                mode: str,
                reply_expected: bool,
                sequence_byte: int,
                command1: int,
                command2: int,
                data=None):
        """Donne un ordre au DMD.

        Les différents ordres que l'on peut envoyer au DMD sont fournis
        sur le guide de Texas Instruments destiné aux programmeurs
        (https://www.ti.com/lit/pdf/dlpu018).

        :param mode: 'r' (lecture) ou 'w' (écriture)
        :param reply_expected: True si on veut une réponse du DMD, False sinon
        :param sequencebyte: identifiant (clé primaire) pour répertorier les
            commandes envoyées (le DMD répondra avec le même identifiant).
        :param command1: Octet le moins significatif (LSB) du code 
            hexadécimal de la commande USB à envoyer (voir guide).
        :param command2: Octet le plus significatif (MSB) du code 
            hexadécimal de la commande USB à envoyer (voir guide).
        :param data: séquence d'octets de données associées à l'ordre
        """

        buffer = [0x00] * 64

        # Gestion du 'flag byte' (cf p16 du guide programmeur dlpu018h.pdf)
        flag_string = ''
        if mode == 'r':
            flag_string += '1'
        else:
            flag_string += '0'

        if reply_expected:
            flag_string += '1'
        else:
            flag_string += '0'
        flag_string += '000000'
        buffer[0] = int(flag_string, 2)

        # Gestion du 'sequence byte'
        buffer[1] = sequence_byte

        # Gestion de la 'data'
        len1 = 2 + len(data)

        if len1 > 254:
            len2 = (2 + len(data)) / 255
            len1 = len1 - len2
        else:
            len2 = 0

        buffer[2] = len1
        buffer[3] = len2
        buffer[4] = com2
        buffer[5] = com1
        for i in range(len(data)):
            buffer[6 + i] = data[i]

        self.device.write(1, buffer)

    def read_reply(self):
        a = self.device.read(0x81, 64)

        for i in a:
            print(hex(i))

    def idle_on(self):
        self.command('w', False, 0x00, 0x02, 0x01, [int('00000001', 2)])

    def idle_off(self):
        self.command('w', False, 0x00, 0x02, 0x01, [int('00000000', 2)])

    def standby(self):
        self.command('w', False, 0x00, 0x02, 0x00, [int('00000001', 2)])

    def wakeup(self):
        self.command('w', False, 0x00, 0x02, 0x00, [int('00000000', 2)])

    def test_read(self):
        self.command('r', True, 0xff, 0x11, 0x00, [])
        self.read_reply()

    def test_write(self):
        self.command('w', True, 0x22, 0x11, 0x00, [0xff, 0x01, 0xff, 0x01, 0xff, 0x01])

    def change_mode(self, mode):
        """Change le mode d'affichage du DMD.
        0 : mode vidéo
        1 : mode pattern pré-chargé (seules les images chargées au préalable
                                     sur la mémoire flash du DMD avec le 
                                     logiciel de Texas Instruments peuvent 
                                     être utilisées).
        2 : mode pattern vidéo
        3 : mode "à la volée" (permet de charger des images sur le DMD 
                               depuis USB/I2C).

        Le mode 3 est celui utilisé pour cette application.
        """
        self.command('w', 0x00, 0x1a, 0x1b, [mode])

    def configurelut(self, number_of_images, number_of_repetitions):
        img = to_bitstring(number_of_images, 11)
        repeat = to_bitstring(number_of_repetitions, 32)

        string = repeat + '00000' + img

        bytes = bits_to_bytes(string)

        self.command('w', 0x00, 0x1a, 0x31, bytes)
        self.command('w', 0x00, 0x1a, 0x31, bytes)

    def define_pattern(self, index, exposure, bitdepth, color, triggerin, darktime, triggerout, patind, bitpos):
        payload = []
        index = to_bitstring(index, 16)
        index = bits_to_bytes(index)
        for i in range(len(index)):
            payload.append(index[i])

        exposure = to_bitstring(exposure, 24)
        exposure = bits_to_bytes(exposure)
        for i in range(len(exposure)):
            payload.append(exposure[i])
        optionsbyte = ''
        optionsbyte += '1'
        bitdepth = to_bitstring(bitdepth - 1, 3)
        optionsbyte = bitdepth + optionsbyte
        optionsbyte = color + optionsbyte
        if triggerin:
            optionsbyte = '1' + optionsbyte
        else:
            optionsbyte = '0' + optionsbyte

        payload.append(bits_to_bytes(optionsbyte)[0])

        darktime = to_bitstring(darktime, 24)
        darktime = bits_to_bytes(darktime)
        for i in range(len(darktime)):
            payload.append(darktime[i])

        triggerout = to_bitstring(triggerout, 8)
        triggerout = bits_to_bytes(triggerout)
        payload.append(triggerout[0])

        patind = to_bitstring(patind, 11)
        bitpos = to_bitstring(bitpos, 5)
        lastbits = bitpos + patind
        lastbits = bits_to_bytes(lastbits)
        for i in range(len(lastbits)):
            payload.append(lastbits[i])

        self.command('w', 0x00, 0x1a, 0x34, payload)

    def init_bmp_load(self, index: int, size: int):
        """Initie le chargement de l'image BMP compressée en codage RLE d'un
        pattern.

        Cette commande est toujours suivie du chargement de l'image du pattern
        en elle-même (fonction bmp_load).

        :param index: indice du pattern dont on souhaite charger l'image
        :param size: nombre d'octets composant l'image compressée + 48 
            octets d'en-tête.
        """

        payload = []

        # Envoi de l'indice au DMD sous la forme appropriée (chaîne d'octets)
        index = to_bitstring(index, 5)
        index = '0' * 11 + index
        index = bits_to_bytes(index)
        for i in range(len(index)):
            payload.append(index[i])

        # Envoi de la taille du pattern
        total_size = to_bitstring(size, 32)
        total_size = bits_to_bytes(total_size)
        for i in range(len(total_size)):
            payload.append(total_size[i])

        self.command('w', 0x00, 0x1a, 0x2a, payload)

    def bmp_load(self, image: str, size: int):
        """Charge l'image BMP compressée en codage RLE du pattern sélectionné
        par la fonction init_bmp_load par paquets de 504 octets.

        :param image: chaîne de caractères représentant l'image BMP compressée
            en codage RLE du pattern sélectionné.
        :param size: nombre d'octets composant l'image compressée + 48 
            octets d'en-tête.
        """

        number_of_packets = size // 504 + 1

        # Compteur du nombre de bits envoyés
        counter = 0

        for i in range(number_of_packets):
            payload = []

            if i < number_of_packets - 1:
                length = to_bitstring(504, 16)
                bits = 504
            else:  # Dernier paquet
                length = to_bitstring(size % 504, 16)
                bits = size % 504

            length = bits_to_bytes(length)

            for j in range(2):
                payload.append(length[j])
            for j in range(bits):
                payload.append(image[counter])
                counter += 1

            self.command('w', 0x11, 0x1a, 0x2b, payload)

    def def_sequence(self, images, exposure_times, triggers_in, dark_times, triggers_out, number_of_repetitions):
        """Définit une séquence (ensemble de patterns).

        :param images: tableau contenant les images BMP non-compressées.
        :param exposure_times: tableau contenant les temps d'exposition en us pour
            chaque image.
        :param triggers_in: tableau de booléens (True si utilisation de Trigger Inputs, False sinon)
        :param dark_times: tableau contenant les temps de temporisation en us (le DMD se met en veille) après chaque image
        :param triggers_out: tableau de booléens (True si utilisation de Trigger Out, False sinon)
        :param number_of_repetitions: nombre de répétitions de la séquence souhaité (0 pour répétition infinie)
        """

        self.stopsequence()

        number_of_images = len(images)
        encoded_images = []
        sizes = []

        for i in range(number_of_images):

            # Fusion des bits d'une même image dans un seul tableau
            if i < number_of_images - 1:
                imagedata = images[i * 24:(i + 1) * 24]
            else:  # Dernière image
                imagedata = images[i * 24:]

            # Compression en RLE des images fusionnées
            imagedata, size = encode(imagedata)

            encoded_images.append(imagedata)
            sizes.append(size)

            # Création d'un pattern pour chaque image
            if i < number_of_images - 1:
                for j in range(i * 24, (i + 1) * 24):
                    self.define_pattern(j,
                                       exposure_times[j],
                                       1, '111',
                                       triggers_in[j],
                                       dark_times[j],
                                       triggers_out[j],
                                       i, j - i * 24)
            else:  # Dernière image
                for j in range(i * 24, number_of_images):
                    self.define_pattern(j,
                                       exposure_times[j],
                                       1, '111',
                                       triggers_in[j],
                                       dark_times[j],
                                       triggers_out[j],
                                       i, j - i * 24)

        self.configurelut(number_of_images, number_of_repetitions)

        for i in range(number_of_images):
            self.init_bmp_load(number_of_images - 1 - i, sizes[number_of_images - 1 - i])

            print('image ' + str(i) + ' en cours de chargement')
            self.bmp_load(encoded_images[number_of_images - 1 - i], sizes[number_of_images - 1 - i])


    def start_sequence(self):
        self.command('w', 0x00, 0x1a, 0x24, [2])


    def pause_sequence(self):
        self.command('w', 0x00, 0x1a, 0x24, [1])


    def stop_sequence(self):
        self.command('w', 0x00, 0x1a, 0x24, [0])
