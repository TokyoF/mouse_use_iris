"""
Script para cambiar el perfil de sensibilidad del sistema
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.config import Config


def main():
    config = Config()
    
    print("=" * 60)
    print("CONFIGURACIÓN DE SENSIBILIDAD - Gaze Control v2.0")
    print("=" * 60)
    
    # Mostrar perfil actual
    current_gain = config.get('gain')
    current_deadzone = config.get('deadzone')
    
    print(f"\nConfiguración actual:")
    print(f"  Gain (sensibilidad): {current_gain}")
    print(f"  Deadzone (zona muerta): {current_deadzone}")
    
    # Identificar perfil más cercano
    current_profile = "personalizado"
    for name, profile in config.SENSITIVITY_PROFILES.items():
        if abs(profile['gain'] - current_gain) < 0.1 and abs(profile['deadzone'] - current_deadzone) < 0.003:
            current_profile = name
            break
    
    print(f"  Perfil actual: {current_profile.upper()}")
    
    # Mostrar perfiles disponibles
    config.list_sensitivity_profiles()
    
    print("\nOpciones:")
    print("1. Aplicar perfil CONSERVATIVE (lento y preciso)")
    print("2. Aplicar perfil BALANCED (equilibrado)")
    print("3. Aplicar perfil PERFORMANCE (rápido - recomendado)")
    print("4. Aplicar perfil EXTREME (ultra rápido)")
    print("5. Configuración manual")
    print("6. Salir sin cambios")
    
    choice = input("\nSelecciona una opción (1-6): ").strip()
    
    if choice == "1":
        config.apply_sensitivity_profile('conservative')
        print("\n✓ Perfil CONSERVATIVE aplicado")
    elif choice == "2":
        config.apply_sensitivity_profile('balanced')
        print("\n✓ Perfil BALANCED aplicado")
    elif choice == "3":
        config.apply_sensitivity_profile('performance')
        print("\n✓ Perfil PERFORMANCE aplicado")
    elif choice == "4":
        config.apply_sensitivity_profile('extreme')
        print("\n✓ Perfil EXTREME aplicado")
    elif choice == "5":
        manual_config(config)
    elif choice == "6":
        print("\nSin cambios")
        return
    else:
        print("\n✗ Opción inválida")
        return
    
    print("\nReinicia la aplicación para aplicar los cambios:")
    print("  python main.py")
    print("=" * 60)


def manual_config(config: Config):
    """Configuración manual de parámetros"""
    print("\n" + "=" * 60)
    print("CONFIGURACIÓN MANUAL")
    print("=" * 60)
    
    try:
        print("\nGain (sensibilidad del cursor):")
        print("  Rango recomendado: 0.8 - 2.5")
        print("  Valor actual:", config.get('gain'))
        gain_input = input("  Nuevo valor (Enter para mantener): ").strip()
        if gain_input:
            gain = float(gain_input)
            if 0.5 <= gain <= 3.0:
                config.set('gain', gain)
                print(f"  ✓ Gain configurado a {gain}")
            else:
                print("  ✗ Valor fuera de rango (0.5-3.0)")
        
        print("\nDeadzone (zona muerta - menor = más sensible):")
        print("  Rango recomendado: 0.005 - 0.025")
        print("  Valor actual:", config.get('deadzone'))
        deadzone_input = input("  Nuevo valor (Enter para mantener): ").strip()
        if deadzone_input:
            deadzone = float(deadzone_input)
            if 0.003 <= deadzone <= 0.050:
                config.set('deadzone', deadzone)
                print(f"  ✓ Deadzone configurado a {deadzone}")
            else:
                print("  ✗ Valor fuera de rango (0.003-0.050)")
        
        print("\nFilter Min Cutoff (suavizado - mayor = menos suavizado):")
        print("  Rango recomendado: 0.5 - 3.0")
        print("  Valor actual:", config.get('filter_min_cutoff'))
        cutoff_input = input("  Nuevo valor (Enter para mantener): ").strip()
        if cutoff_input:
            cutoff = float(cutoff_input)
            if 0.3 <= cutoff <= 5.0:
                config.set('filter_min_cutoff', cutoff)
                print(f"  ✓ Filter Min Cutoff configurado a {cutoff}")
            else:
                print("  ✗ Valor fuera de rango (0.3-5.0)")
        
        print("\nFilter Beta (respuesta a velocidad):")
        print("  Rango recomendado: 0.02 - 0.15")
        print("  Valor actual:", config.get('filter_beta'))
        beta_input = input("  Nuevo valor (Enter para mantener): ").strip()
        if beta_input:
            beta = float(beta_input)
            if 0.01 <= beta <= 0.20:
                config.set('filter_beta', beta)
                print(f"  ✓ Filter Beta configurado a {beta}")
            else:
                print("  ✗ Valor fuera de rango (0.01-0.20)")
        
        config.save()
        print("\n✓ Configuración manual guardada")
        
    except ValueError:
        print("\n✗ Error: Ingresa valores numéricos válidos")


if __name__ == "__main__":
    main()
