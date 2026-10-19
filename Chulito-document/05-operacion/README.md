# 05-operacion

- `entregas/entrega-vX.Y_AAAA-MM-DD/`: copia congelada de cada entrega con su `.zip` (tal como se recibió) y su `MANIFEST_SHA256.txt`.
- Futuro: runbooks de despliegue y operación. Los `.zip` de cada entrega están fuera del repositorio, en `C:\dev\Chulito_documentos\Chulito-document\05-operacion\entregas\`; aquí quedan el `README.md` y el `MANIFEST_SHA256.txt`.

Verificar integridad en PowerShell: `Get-FileHash -Algorithm SHA256 <archivo>` y comparar con el manifiesto.
