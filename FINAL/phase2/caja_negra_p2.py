import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

def evaluar_y_generar_submission(
    X_train,
    y_train,
    X_test,
    test_user_ids,
    output_path="submission_p2.csv"
):
    """
    Modelo de Caja Negra oficial para la Competencia Etapa 2.
    NO MODIFICAR este archivo. Su reto es mejorar el Feature Vector (X_train / X_test).
    """
    print("=" * 65)
    print("📦 MODELO CAJA NEGRA - ETAPA 2 (OPERACIÓN CAZADORES DE BOTS)")
    print("=" * 65)

    # Convertir a DataFrame si viene como ndarray para validar fácilmente
    X_tr = pd.DataFrame(X_train).copy()
    X_te = pd.DataFrame(X_test).copy()
    y_tr = pd.Series(y_train).values
    ids_te = pd.Series(test_user_ids).values

    # 1. Validaciones de dimensiones
    if len(X_tr) != 700 or len(y_tr) != 700:
        raise ValueError(f"❌ X_train y y_train deben tener exactamente 700 filas (tienen {len(X_tr)} y {len(y_tr)}).")
    if len(X_te) != 300 or len(ids_te) != 300:
        raise ValueError(f"❌ X_test y test_user_ids deben tener exactamente 300 filas (tienen {len(X_te)} y {len(ids_te)}).")
    if X_tr.shape[1] != X_te.shape[1]:
        raise ValueError(f"❌ X_train ({X_tr.shape[1]} cols) y X_test ({X_te.shape[1]} cols) deben tener las mismas columnas.")
    if list(X_tr.columns) != list(X_te.columns):
        raise ValueError("❌ El orden o nombre de las columnas en X_train y X_test no coincide.")

    # 2. Validación de tipos numéricos (sin strings sin codificar)
    non_num_tr = X_tr.select_dtypes(exclude=[np.number, bool]).columns.tolist()
    non_num_te = X_te.select_dtypes(exclude=[np.number, bool]).columns.tolist()
    if non_num_tr or non_num_te:
        raise TypeError(
            f"❌ La Caja Negra solo acepta variables numéricas. "
            f"Aún tienes texto sin codificar en: {sorted(list(set(non_num_tr + non_num_te)))}"
        )

    # 3. Validación de NaNs e Infinitos
    if X_tr.isna().any().any() or X_te.isna().any().any():
        raise ValueError("❌ Se detectaron valores NaN en X_train o X_test. Revisa tus transformaciones/ratios.")
    if np.isinf(X_tr.to_numpy(dtype=float)).any() or np.isinf(X_te.to_numpy(dtype=float)).any():
        raise ValueError("❌ Se detectaron valores infinitos (inf/-inf). ¿Dividiste entre cero en algún ratio?")

    # 4. Modelo fijo (semilla e hiperparámetros bloqueados)
    modelo = LogisticRegression(
        C=0.5,
        max_iter=300,
        random_state=42,
        class_weight="balanced"
    )

    # 5. Validación Cruzada Local (5-Fold Stratified)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(modelo, X_tr, y_tr, cv=cv, scoring="f1_macro")
    mean_f1 = float(np.mean(scores))
    std_f1 = float(np.std(scores))

    # 6. Entrenamiento final y predicción sobre test_p2.csv
    modelo.fit(X_tr, y_tr)
    preds = modelo.predict(X_te).astype(int)

    df_sub = pd.DataFrame({
        "user_id": ids_te,
        "is_bot": preds
    })
    df_sub.to_csv(output_path, index=False)

    print(f"📐 Dimensiones del Feature Vector : {X_tr.shape[1]} features")
    print(f"🎯 CV Local (5-Fold Macro F1)     : {mean_f1:.4f} (+/- {std_f1:.4f})")
    print(f"🤖 Predicciones en Test           : {(preds == 1).sum()} bots | {(preds == 0).sum()} humanos")
    print(f"💾 Archivo generado               : {output_path}")
    if mean_f1 < 0.70:
        print("🟡 Sugerencia: Estás en zona Baseline. Revisa los encodings, escalamiento y pistas del acertijo.")
    elif mean_f1 < 0.85:
        print("🟠 Buen avance: Ya superaste el Baseline, pero aún hay señal oculta (ratios / clustering).")
    else:
        print("🟢 ¡Excelente Feature Engineering! Tu vector ya desbloqueó la señal de alto nivel.")
    print("=" * 65)
    return mean_f1, df_sub
