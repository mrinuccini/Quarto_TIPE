from random import getrandbits

class Zobrist:
    def __init__(self):
        self.table_plateau = [[getrandbits(64) for _ in range(16)] for _ in range(16)] # Génère les hash de départ pour 16 pièces * 16 cases
        self.table_main = [getrandbits(64) for _ in range(16)]
        self.table_trait = getrandbits(64)

        self.hash_actuels = [0 for _ in range(8)]
        self.piece_en_main = None
        self.sym = self._generer_table_symetries()

    def debut(self, piece_debut_id: int) -> int:
        self.piece_en_main = piece_debut_id
        self.hash_actuels[0] ^= self.table_main[piece_debut_id]
    
    def _generer_table_symetries(self):
        sym = [[0] * 16 for _ in range(8)]
        for i in range(16):
            x, y = i % 4, i // 4
            sym[0][i] = i                               # 0. Identité
            sym[1][i] = (3 - y) + x * 4                 # 1. Rotation 90°
            sym[2][i] = (3 - x) + (3 - y) * 4           # 2. Rotation 180°
            sym[3][i] = y + (3 - x) * 4                 # 3. Rotation 270°
            sym[4][i] = (3 - x) + y * 4                 # 4. Miroir Horizontal
            sym[5][i] = x + (3 - y) * 4                 # 5. Miroir Vertical
            sym[6][i] = y + x * 4                       # 6. Diagonale principale
            sym[7][i] = (3 - y) + (3 - x) * 4           # 7. Anti-diagonale
        return sym

    def placer_piece(self, case: int):
        for i in range(8):
            case_sym = self.sym[i][case]

            self.hash_actuels[i] ^= self.table_plateau[self.piece_en_main][case_sym]
            self.hash_actuels[i] ^= self.table_main[self.piece_en_main]

    def choisir_piece(self, nouvelle_piece: int):
        for i in range(8):
            if nouvelle_piece is not None:
                self.piece_en_main = nouvelle_piece
                self.hash_actuels[i] ^= self.table_main[nouvelle_piece]
            else:
                self.piece_en_main = None

            self.hash_actuels[i] ^= self.table_trait

    def jouer_coup(self, case: int, nouvelle_piece: int) -> int:
        for i in range(8):
            case_sym = self.sym[i][case]

            self.hash_actuels[i] ^= self.table_plateau[self.piece_en_main][case_sym]
            self.hash_actuels[i] ^= self.table_main[self.piece_en_main]

            if nouvelle_piece is not None:
                self.piece_en_main = nouvelle_piece
                self.hash_actuels[i] ^= self.table_main[nouvelle_piece]
            else:
                self.piece_en_main = None

            self.hash_actuels[i] ^= self.table_trait

    def get_canonical_hash(self): return min(self.hash_actuels)
