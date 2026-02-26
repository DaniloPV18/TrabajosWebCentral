import { LABELS } from "@/constants/labels";
import { useVacantes } from "@/context/VacantesContext";
import { useVacantesData } from "@/hooks/useVacantesData";
import { tieneAlgunFiltro } from "@/lib/utils";
import { COLORS } from "@/constants/colors";

export const FilterSidebar = () => {
  const { busqueda, filtros, setFiltros, limpiarTodo } = useVacantes();
  const { empresas, ubicaciones, areas, modalidades, contadorPorEmpresa } =
    useVacantesData();

  const mostrarBotonLimpiar = tieneAlgunFiltro(filtros, busqueda);

  const handleFiltroChange = (tipo: keyof typeof filtros, valor: string) => {
    if (filtros[tipo] === valor) {
      setFiltros({ ...filtros, [tipo]: "" });
    } else {
      setFiltros({ ...filtros, [tipo]: valor });
    }
  };

  return (
    <aside className="lg:col-span-1">
        <div className={`${COLORS.bg.secondary} rounded-xl shadow-xl p-6 sticky top-24 border ${COLORS.border.light} overflow-hidden`} role="region" aria-label="Filtros de búsqueda">
          {/* Top border con gradiente */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-violet-500 to-magenta-500"></div>
        
          <div className="flex justify-between items-center mb-6 pb-4 border-b border-slate-700">
            <h2 className={`text-lg font-bold ${COLORS.text.primary}`}>
            ⚙️ {LABELS.FILTROS}
          </h2>
          {mostrarBotonLimpiar && (
            <button
              onClick={limpiarTodo}
                className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold transition-colors px-2 py-1 rounded-md hover:bg-cyan-500/10"
              aria-label="Limpiar todos los filtros"
            >
              {LABELS.LIMPIAR}
            </button>
          )}
        </div>

        {/* Empresas */}
        <FilterSection
          title={LABELS.EMPRESA}
          opciones={empresas}
          selectedValue={filtros.empresa}
          onChange={(valor) => handleFiltroChange("empresa", valor)}
          counter={contadorPorEmpresa}
        />

        {/* Modalidad */}
        <FilterSection
          title={LABELS.MODALIDAD}
          opciones={modalidades}
          selectedValue={filtros.modalidad}
          onChange={(valor) => handleFiltroChange("modalidad", valor)}
        />

        {/* Área */}
        <FilterSection
          title={LABELS.AREA}
          opciones={areas}
          selectedValue={filtros.area}
          onChange={(valor) => handleFiltroChange("area", valor)}
          maxHeight
        />

        {/* Ubicación */}
        <FilterSection
          title={LABELS.UBICACION}
          opciones={ubicaciones}
          selectedValue={filtros.ubicacion}
          onChange={(valor) => handleFiltroChange("ubicacion", valor)}
          maxHeight
        />
      </div>
    </aside>
  );
};

interface FilterSectionProps {
  title: string;
  opciones: string[];
  selectedValue: string;
  onChange: (valor: string) => void;
  counter?: Record<string, number>;
  maxHeight?: boolean;
}

const FilterSection = ({
  title,
  opciones,
  selectedValue,
  onChange,
  counter,
  maxHeight,
}: FilterSectionProps) => {
  return (
    <div className="mb-6">
      <h3 className={`text-sm font-semibold ${COLORS.text.secondary} mb-3 uppercase tracking-wider`}>{title}</h3>
      <div className={`space-y-2 ${maxHeight ? "max-h-48 overflow-y-auto" : ""}`}>
        {opciones.map((opcion) => (
          <label
            key={opcion}
            className={`flex items-center gap-2 cursor-pointer p-2 rounded-lg transition-all ${selectedValue === opcion ? `${COLORS.bg.tertiary} border-l-2 border-cyan-400` : `${COLORS.text.secondary} hover:${COLORS.bg.tertiary}`}`}
          >
            <input
              type="radio"
              name={title.toLowerCase()}
              checked={selectedValue === opcion}
              onChange={() => onChange(opcion)}
              className="cursor-pointer accent-cyan-400"
              aria-label={`Filtrar por ${title.toLowerCase()}: ${opcion}`}
            />
            <span className={`text-sm flex-1 ${selectedValue === opcion ? "text-cyan-300 font-semibold" : COLORS.text.secondary}`}>{opcion}</span>
            {counter && counter[opcion] && (
              <span
                className="text-xs bg-violet-500/30 text-violet-300 px-2 py-1 rounded-full border border-violet-500/50 font-semibold"
                aria-label={`${counter[opcion]} vacantes`}
              >
                {counter[opcion]}
              </span>
            )}
          </label>
        ))}
      </div>
    </div>
  );
};
