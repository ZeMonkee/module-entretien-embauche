import torch
import os

print("--- Démarrage du téléchargement des modèles Bark (Patch PyTorch 2.6) ---")

# --- LE HACK POUR PYTORCH 2.6 ---
# On remplace la fonction de chargement officielle par une version qui désactive la sécurité par défaut
# car les modèles Bark sont plus vieux que cette sécurité.
_original_torch_load = torch.load
def _safe_load_wrapper(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)

torch.load = _safe_load_wrapper
# --------------------------------

from bark import preload_models

print("Reprise du téléchargement...")
print("(Le fichier text.pt de 2Go est probablement déjà là, il va vérifier et passer à la suite)")

# On force le téléchargement CPU
preload_models(
    text_use_gpu=False,
    text_use_small=True,
    coarse_use_gpu=False,
    coarse_use_small=True,
    fine_use_gpu=False,
    fine_use_small=True,
    codec_use_gpu=False
)

print("✅ TÉLÉCHARGEMENT TERMINÉ ! Les fichiers sont validés.")
