import os
import sys
import pandas as pd
import numpy as np

def validar_etapa_1(
    path_maestro="maestro_usuarios_limpio.csv",
    path_red="red_interacciones_limpia.csv",
    path_sub="submission_p1.csv"
):
    print("="*60)
    print("🚦 VALIDADOR AUTOMÁTICO - ETAPA 1 (OPERACIÓN CAZADORES DE BOTS)")
    print("="*60)
    errores = []

    # 1. Existencia de archivos
    for p in [path_maestro, path_red, path_sub]:
        if not os.path.exists(p):
            errores.append(f"❌ No se encontró el archivo requerido: {p}")
    if errores:
        for e in errores: print(e)
        print("\n🔴 LUZ ROJA: Genera todos los archivos requeridos antes de validar.")
        return False

    df_m = pd.read_csv(path_maestro)
    df_r = pd.read_csv(path_red)
    df_s = pd.read_csv(path_sub)

    # 2. Validación de Esquema en maestro_usuarios_limpio.csv
    cols_esperadas = {
        "user_id", "fecha_creacion", "edad_usuario", "pais", "dispositivo",
        "nivel_verificacion", "seguidores", "siguiendo", "posts_totales",
        "tasa_interaccion", "hora_pico_actividad", "email_domain",
        "last_ip", "payment_hash", "avg_session_min",
        "variance_post_interval_hr", "likes_given_30d"
    }
    if "version_api" in df_m.columns:
        errores.append("❌ La columna constante 'version_api' debe ser eliminada (Reducción de datos).")
    
    faltantes = cols_esperadas - set(df_m.columns)
    if faltantes:
        errores.append(f"❌ Faltan columnas en {path_maestro}: {sorted(list(faltantes))}")

    # 3. Validación de Nulos (payment_hash puede ser 'SIN_TARJETA' o similar, pero sin NaN)
    nulos_m = df_m.isna().sum()
    cols_con_nulos = nulos_m[nulos_m > 0].to_dict()
    if cols_con_nulos:
        errores.append(f"❌ Aún existen valores nulos en {path_maestro}: {cols_con_nulos}")

    # Verificar que no queden textos centinela ("N/A", "-999")
    for col in df_m.select_dtypes(include="object").columns:
        if df_m[col].astype(str).str.strip().isin(["N/A", "n/a", "-999", ""]).any():
            errores.append(f"❌ Se detectaron nulos disfrazados ('N/A', '-999' o vacíos) en columna '{col}'.")

    # 4. Duplicados y Estandarización
    if df_m["user_id"].duplicated().any():
        errores.append("❌ Existen 'user_id' duplicados en maestro_usuarios_limpio.csv.")
    if (df_m["user_id"] != df_m["user_id"].astype(str).str.strip().str.upper()).any():
        errores.append("❌ 'user_id' no está estandarizado (mayúsculas y sin espacios).")

    paises_ok = {"MEXICO", "ARGENTINA", "COLOMBIA", "ESPANA", "CHILE"}
    if "pais" in df_m.columns and not set(df_m["pais"].unique()).issubset(paises_ok):
        errores.append(f"❌ Valores no estandarizados en 'pais': {set(df_m['pais'].unique()) - paises_ok}")

    disps_ok = {"ANDROID", "IOS", "WEB", "API_SCRIPT"}
    if "dispositivo" in df_m.columns and not set(df_m["dispositivo"].unique()).issubset(disps_ok):
        errores.append(f"❌ Valores no estandarizados en 'dispositivo': {set(df_m['dispositivo'].unique()) - disps_ok}")

    verif_ok = {"NINGUNO", "CORREO", "TELEFONO", "VERIFICADO"}
    if "nivel_verificacion" in df_m.columns and not set(df_m["nivel_verificacion"].unique()).issubset(verif_ok):
        errores.append(f"❌ Valores no estandarizados en 'nivel_verificacion': {set(df_m['nivel_verificacion'].unique()) - verif_ok}")

    # 5. Rangos Lógicos y Fechas
    try:
        fechas = pd.to_datetime(df_m["fecha_creacion"], format="%Y-%m-%d", errors="raise")
        if (fechas > pd.Timestamp("2026-11-23")).any():
            errores.append("❌ Existen fechas futuras (> 2026-11-23) en 'fecha_creacion'.")
    except Exception:
        errores.append("❌ 'fecha_creacion' debe estar en formato estándar ISO YYYY-MM-DD.")

    if ((df_m["edad_usuario"] < 13) | (df_m["edad_usuario"] > 100)).any():
        errores.append("❌ Existen edades imposibles (< 13 o > 100) en 'edad_usuario'.")
    if ((df_m["seguidores"] < 0) | (df_m["seguidores"] > 10_000_000)).any():
        errores.append("❌ Existen valores imposibles en 'seguidores' (< 0 o > 10,000,000).")
    if ((df_m["tasa_interaccion"] < 0) | (df_m["tasa_interaccion"] > 1.0)).any():
        errores.append("❌ Existen valores fuera de rango [0, 1] en 'tasa_interaccion'.")
    if (df_m["avg_session_min"] <= 0).any():
        errores.append("❌ Existen valores <= 0 (o -999 sin limpiar) en 'avg_session_min'.")

    # 6. Validación de red_interacciones_limpia.csv
    if not {"origen", "destino", "tipo_relacion"}.issubset(set(df_r.columns)):
        errores.append("❌ red_interacciones_limpia.csv debe tener las columnas: ['origen', 'destino', 'tipo_relacion'].")
    else:
        if (df_r["origen"] == df_r["destino"]).any():
            errores.append("❌ Existen self-loops (origen == destino) en red_interacciones_limpia.csv.")
        if df_r.duplicated(subset=["origen", "destino", "tipo_relacion"]).any():
            errores.append("❌ Existen aristas duplicadas en red_interacciones_limpia.csv.")
        valid_set = set(df_m["user_id"])
        if not set(df_r["origen"]).issubset(valid_set) or not set(df_r["destino"]).issubset(valid_set):
            errores.append("❌ La red contiene nodos que NO existen en maestro_usuarios_limpio.csv.")

    # 7. Validación de formato de submission_p1.csv para Kaggle
    if list(df_s.columns) != ["row_id", "estado_auditoria"]:
        errores.append("❌ submission_p1.csv debe tener exactamente las columnas: ['row_id', 'estado_auditoria'].")
    elif len(df_s) != 1250:
        errores.append(f"❌ submission_p1.csv debe tener exactamente 1250 filas (tiene {len(df_s)}).")
    elif not set(df_s["estado_auditoria"].unique()).issubset({0, 1, 2}):
        errores.append("❌ 'estado_auditoria' solo puede contener los valores enteros {0, 1, 2}.")

    # Veredicto Final
    print(f"📊 Resumen: {len(df_m)} usuarios limpios | {len(df_r)} aristas limpias | {len(df_s)} filas en submission.")
    if not errores:
        print("\n🟢 LUZ VERDE: ¡Todas las pruebas de calidad pasaron al 100%!")
        print("   -> Tus datasets están listos para Etapa 2 y Etapa 3.")
        print("   -> Ya puedes subir 'submission_p1.csv' a Kaggle.")
        return True
    else:
        print("\n🔴 LUZ ROJA: Se encontraron los siguientes problemas:")
        for e in errores:
            print("  ", e)
        return False

if __name__ == "__main__":
    ok = validar_etapa_1()
    sys.exit(0 if ok else 1)
