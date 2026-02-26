// app/__tests__/page.test.tsx
import { filtrarVacantes, formatFecha, tieneAlgunFiltro } from "@/lib/utils";
import { vacantesData } from "@/data/vacantes";

describe("Utility Functions", () => {
  describe("formatFecha", () => {
    it("debe formatear la fecha correctamente", () => {
      const fecha = "2024-02-25";
      const resultado = formatFecha(fecha);
      expect(resultado).toContain("2024");
      expect(resultado).toContain("25");
    });
  });

  describe("filtrarVacantes", () => {
    it("debe retornar todas las vacantes si no hay búsqueda ni filtros", () => {
      const filtros = {
        empresa: "",
        ubicacion: "",
        modalidad: "",
        area: "",
      };
      const resultado = filtrarVacantes(vacantesData, "", filtros);
      expect(resultado.length).toBe(vacantesData.length);
    });

    it("debe filtrar vacantes por búsqueda de título", () => {
      const filtros = {
        empresa: "",
        ubicacion: "",
        modalidad: "",
        area: "",
      };
      const resultado = filtrarVacantes(
        vacantesData,
        "Ingeniero",
        filtros
      );
      expect(resultado.length).toBeGreaterThan(0);
      expect(resultado[0].titulo).toContain("Ingeniero");
    });

    it("debe filtrar vacantes por empresa", () => {
      const filtros = {
        empresa: "Grupo Palmon",
        ubicacion: "",
        modalidad: "",
        area: "",
      };
      const resultado = filtrarVacantes(vacantesData, "", filtros);
      expect(resultado.every((v) => v.empresa === "Grupo Palmon")).toBe(true);
    });

    it("debe filtrar vacantes por modalidad", () => {
      const filtros = {
        empresa: "",
        ubicacion: "",
        modalidad: "Remoto",
        area: "",
      };
      const resultado = filtrarVacantes(vacantesData, "", filtros);
      expect(resultado.every((v) => v.modalidad === "Remoto")).toBe(true);
    });
  });

  describe("tieneAlgunFiltro", () => {
    it("debe retornar false si no hay filtros ni búsqueda", () => {
      const filtros = {
        empresa: "",
        ubicacion: "",
        modalidad: "",
        area: "",
      };
      expect(tieneAlgunFiltro(filtros, "")).toBe(false);
    });

    it("debe retornar true si hay búsqueda", () => {
      const filtros = {
        empresa: "",
        ubicacion: "",
        modalidad: "",
        area: "",
      };
      expect(tieneAlgunFiltro(filtros, "ingeniero")).toBe(true);
    });

    it("debe retornar true si hay filtros activos", () => {
      const filtros = {
        empresa: "Grupo Palmon",
        ubicacion: "",
        modalidad: "",
        area: "",
      };
      expect(tieneAlgunFiltro(filtros, "")).toBe(true);
    });
  });
});
