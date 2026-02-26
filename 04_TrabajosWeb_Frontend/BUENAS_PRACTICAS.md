# Frontend - Buenas Prácticas Implementadas

## 📁 Estructura de Carpetas

```
src/
├── app/                      # App Router de Next.js
│   ├── __tests__/           # Tests unitarios
│   ├── layout.tsx           # Layout raíz
│   ├── page.tsx             # Página principal (limpia)
│   └── globals.css          # Estilos globales
├── components/              # Componentes reutilizables
│   ├── Header.tsx           # Encabezado principal
│   ├── SearchBar.tsx        # Barra de búsqueda
│   ├── FilterSidebar.tsx    # Panel de filtros
│   ├── VacanteCard.tsx      # Tarjeta de vacante
│   ├── VacanteList.tsx      # Lista de vacantes
│   └── EmptyState.tsx       # Estado vacío
├── context/                 # Contexto global
│   └── VacantesContext.tsx  # Context para estado de búsqueda/filtros
├── hooks/                   # Custom hooks
│   ├── useFilteredVacantes.ts   # Lógica de filtrado
│   └── useVacantesData.ts       # Datos de vacantes
├── data/                    # Datos quemados
│   └── vacantes.ts          # Array de vacantes + funciones helper
├── lib/                     # Funciones utilitarias
│   └── utils.ts             # Funciones puras para lógica de negocios
├── constants/               # Constantes
│   ├── colors.ts            # Colores y clases CSS
│   └── labels.ts            # Labels y mensajes
└── types/                   # Tipos TypeScript
    └── index.ts             # Interfaces principales
```

## ✨ Buenas Prácticas Aplicadas

### 1. **Separation of Concerns**
- **Components**: Solo responsables de renderizar UI
- **Hooks**: Contenedor de lógica reutilizable
- **Context**: Estado global (búsqueda, filtros)
- **Utilities**: Funciones puras sin efectos secundarios
- **Constants**: Valores inmutables centralizados

### 2. **TypeScript Strict**
```typescript
// ✅ Tipos bien definidos
interface Vacante {
  id: number;
  titulo: string;
  // ...
}

// ✅ Props tipadas en componentes
interface HeaderProps {
  totalVacantes: number;
}
```

### 3. **React Context API**
En lugar de prop drilling, usamos Context para compartir estado:
```typescript
export const useVacantes = () => {
  const context = useContext(VacantesContext);
  if (context === undefined) {
    throw new Error("useVacantes must be used within VacantesProvider");
  }
  return context;
};
```

### 4. **Custom Hooks para Lógica Reutilizable**
```typescript
// hooks/useFilteredVacantes.ts - Lógica de filtrado memoizada
export const useFilteredVacantes = (busqueda: string, filtros: any) => {
  const vacantesFiltered = useMemo(() => {
    return filtrarVacantes(vacantesData, busqueda, filtros);
  }, [busqueda, filtros]);
  return vacantesFiltered;
};
```

### 5. **Composición de Componentes**
```typescript
// page.tsx - Limpio y legible
<Header totalVacantes={totalVacantes} />
<SearchBar />
<FilterSidebar />
<VacanteList vacantes={vacantes} totalVacantes={totalVacantes} />
```

### 6. **Funciones Puras**
```typescript
// lib/utils.ts - Sin efectos secundarios
export const filtrarVacantes = (vacantes, busqueda, filtros) => {
  return vacantes.filter(/* ... */);
};

export const formatFecha = (fecha: string): string => {
  return new Date(fecha).toLocaleDateString("es-ES", /* ... */);
};
```

### 7. **DRY (Don't Repeat Yourself)**
- **Constantes**: `LABELS`, `MODALIDAD_COLORS` centralizadas
- **Funciones**: Helper functions para lógica común
- **Tipos**: Una fuente de verdad en `types/index.ts`

### 8. **Performance**
```typescript
// useMemo para evitar re-especialización innecesaria
const vacantes = useMemo(() => {
  return filtrarVacantes(vacantesData, busqueda, filtros);
}, [busqueda, filtros]);

// Hooks memorizados no se recalculan
const { empresas, ubicaciones, areas } = useVacantesData();
```

### 9. **Accesibilidad (a11y)**
```typescript
// ARIA labels y roles semánticos
<input
  type="search"
  aria-label={ARIA_LABELS.SEARCH_INPUT}
  className="..."
/>
<article role="article" aria-label={`Vacante: ${vacante.titulo}`} />
```

### 10. **Semantic HTML**
```typescript
// ✅ Tags semánticos
<header>
<main>
<article>
<aside>
<nav>
<time>
```

### 11. **Mensajes Centralizados**
**constants/labels.ts** contiene TODOS los textos del UI:
```typescript
export const LABELS = {
  TITULO_PORTAL: "TrabajosWeb",
  BUSCAR_PLACEHOLDER: "Busca por título...",
  // ... más labels
};
```
Ventajas:
- ✅ Fácil traducción/i18n en el futuro
- ✅ Consistencia de mensajes
- ✅ Cambios centralizados

## 🧪 Testing

Tests unitarios básicos en `__tests__/page.test.tsx`:
```typescript
describe("filtrarVacantes", () => {
  it("debe filtrar vacantes por empresa", () => {
    const resultado = filtrarVacantes(vacantesData, "", {
      empresa: "Grupo Palmon",
      // ...
    });
    expect(resultado.every(v => v.empresa === "Grupo Palmon")).toBe(true);
  });
});
```

Para ejecutar tests:
```bash
npm run test
```

## 🚀 Escalabilidad Futura

Esta estructura permite:
1. **Agregar filtros nuevos** sin cambiar `page.tsx`
2. **Cambiar fuente de datos** sin refactoring masivo
3. **Implementar i18n** centralizando labels
4. **Agregar temas (dark mode)** en contexto global
5. **Conectar a API backend** sin cambiar componentes

## 📝 Convenciones

- **Componentes**: PascalCase (`VacanteCard.tsx`)
- **Hooks**: Prefijo `use` (`useFilteredVacantes`)
- **Utilities**: camelCase, funciones puras
- **Constantes**: UPPER_CASE
- **Tipos/Interfaces**: PascalCase con sufijo `Props` para componentes

## 📦 Dependencias Principales

- **Next.js 16.1.6**: Framework React
- **TypeScript 5**: Type safety
- **Tailwind CSS 4**: Utility-first CSS
- **React 19**: Última versión

---

**Nota**: Este frontend actualmente usa datos quemados. Para conectar con API backend, actualizar `data/vacantes.ts` para hacer fetch desde `/api/vacantes`.
