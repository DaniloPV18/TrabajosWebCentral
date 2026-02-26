## Environment Setup de Next.js

Este archivo documenta la configuración recomendada para desarrollo.

### .env.local (Crea este archivo)

```env
# Logs Service URL
NEXT_PUBLIC_LOGS_API_URL=http://localhost:8000

# API Backend (cuando esté lista)
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Prettier Configuration (.prettierrc)

Ya configurado para:
- Ancho de línea: 80 caracteres
- Tabs: 2 espacios
- Trailing commas: es5
- Semicolons: true
- Single quotes: false

### ESLint Configuration (eslint.config.mjs)

Incluye:
- next/core-web-vitals
- React best practices
- TypeScript strict mode

### Pre-commit Hooks (Futuro)

Recomendado instalar `husky`:
```bash
npm install husky lint-staged --save-dev
npx husky install
```

Luego crear `.husky/pre-commit`:
```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"
npm run lint
```

### Scripts Available

```bash
npm run dev      # Desarrollo en http://localhost:3000
npm run build    # Compilación para producción
npm start        # Ejecutar build compilado
npm run lint     # Ejecutar ESLint
```

### Debugging

#### VSCode Debugging

Crear `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js Debugging",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

Presionar F5 para debuguear.

#### React DevTools

Instalar extensión de Chrome:
- React Developer Tools

#### Next.js DevTools

El panel en desarrollo (`http://localhost:3000`):
- Hot reload automático
- Fast Refresh
- Source maps para debugging

### Performance Tips

1. **React.lazy + Suspense** para code splitting
2. **useMemo** para cálculos costosos (ya implementado)
3. **useCallback** si pasas callbacks a componentes hijos
4. **Image optimization** con `next/image`
5. **Prefetch** de rutas con `Link prefetch`

---

Para preguntas sobre setup, consultar `BUENAS_PRACTICAS.md`.
