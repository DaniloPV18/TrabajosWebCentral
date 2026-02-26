"use client";

import { Header } from "@/components/Header";
import { SearchBar } from "@/components/SearchBar";
import { FilterSidebar } from "@/components/FilterSidebar";
import { VacanteList } from "@/components/VacanteList";
import { useVacantes } from "@/context/VacantesContext";
import { useFilteredVacantes } from "@/hooks/useFilteredVacantes";
import { useVacantesData } from "@/hooks/useVacantesData";

export default function Home() {
  const { busqueda, filtros, limpiarTodo } = useVacantes();
  const { totalVacantes } = useVacantesData();
  const vacantes = useFilteredVacantes(busqueda, filtros);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950">
      {/* Background Glow Effects */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-96 h-96 bg-violet-500/5 rounded-full filter blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-cyan-500/5 rounded-full filter blur-3xl"></div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <Header totalVacantes={totalVacantes} />

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Barra de Búsqueda */}
        <SearchBar />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Filtros */}
          <FilterSidebar />

          {/* Lista de Vacantes */}
          <VacanteList
            vacantes={vacantes}
            totalVacantes={totalVacantes}
            onLimpiarFiltros={limpiarTodo}
          />
        </div>
      </main>
      </div>
    </div>
  );
}
