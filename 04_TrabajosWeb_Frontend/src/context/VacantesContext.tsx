"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";
import { Filtros } from "@/types";

interface VacantesContextType {
  busqueda: string;
  setBusqueda: (busqueda: string) => void;
  filtros: Filtros;
  setFiltros: (filtros: Filtros) => void;
  limpiarTodo: () => void;
}

const VacantesContext = createContext<VacantesContextType | undefined>(
  undefined
);

export const VacantesProvider = ({ children }: { children: ReactNode }) => {
  const [busqueda, setBusqueda] = useState("");
  const [filtros, setFiltros] = useState<Filtros>({
    empresa: "",
    ubicacion: "",
    modalidad: "",
    area: "",
  });

  const limpiarTodo = () => {
    setBusqueda("");
    setFiltros({
      empresa: "",
      ubicacion: "",
      modalidad: "",
      area: "",
    });
  };

  return (
    <VacantesContext.Provider
      value={{ busqueda, setBusqueda, filtros, setFiltros, limpiarTodo }}
    >
      {children}
    </VacantesContext.Provider>
  );
};

export const useVacantes = () => {
  const context = useContext(VacantesContext);
  if (context === undefined) {
    throw new Error("useVacantes must be used within VacantesProvider");
  }
  return context;
};
