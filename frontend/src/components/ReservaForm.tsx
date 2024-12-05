import React, { useState, useEffect } from "react";
import apiClient from "../api/client";

const ReservaForm = () => {
  const [form, setForm] = useState({
    cancha_id: "",
    dia: "",
    hora: "",
    duracion: "",
    nombre_contacto: "",
    telefono: "",
  });

  const [canchas, setCanchas] = useState<any[]>([]);

  useEffect(() => {
    const fetchCanchas = async () => {
      try {
        const response = await apiClient.get("/api/canchas");
        setCanchas(response.data);
      } catch (error) {
        console.error("Error al obtener las canchas:", error);
      }
    };

    fetchCanchas();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.dia || !form.hora || !form.nombre_contacto || !form.telefono || !form.cancha_id) {
      alert("Todos los campos son obligatorios");
      return;
    }
    try {
      await apiClient.post("/api/reservas", form);
      alert("Reserva creada exitosamente");

      setForm({
        cancha_id: "",
        dia: "",
        hora: "",
        duracion: "",
        nombre_contacto: "",
        telefono: "",
      });
    } catch (error: any) {
      alert(error.response?.data?.detail || "Error al crear la reserva");
    }
  };

  return (
    <div className="container">
      <h2>Crear Reserva</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="cancha_id">Seleccionar Cancha</label>
          {canchas.length > 0 ? (
            <select
              name="cancha_id"
              onChange={handleChange}
              value={form.cancha_id}
              className="form-control"
              required
            >
              <option value="">Seleccionar cancha</option>
              {canchas.map((cancha) => (
                <option key={cancha.id} value={cancha.id}>
                  {cancha.nombre}
                </option>
              ))}
            </select>
          ) : (
            <p>No hay canchas disponibles para reservar</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="dia">Fecha</label>
          <input
            type="date"
            name="dia"
            onChange={handleChange}
            value={form.dia}
            className="form-control"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="hora">Hora</label>
          <input
            type="time"
            name="hora"
            onChange={handleChange}
            value={form.hora}
            className="form-control"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="duracion">Duración</label>
          <input
            type="number"
            name="duracion"
            onChange={handleChange}
            value={form.duracion}
            className="form-control"
            placeholder="Duración en minutos"
          />
        </div>

        <div className="form-group">
          <label htmlFor="nombre_contacto">Nombre</label>
          <input
            type="text"
            name="nombre_contacto"
            onChange={handleChange}
            value={form.nombre_contacto}
            className="form-control"
            placeholder="Nombre del contacto"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="telefono">Teléfono</label>
          <input
            type="text"
            name="telefono"
            onChange={handleChange}
            value={form.telefono}
            className="form-control"
            placeholder="Teléfono"
            required
          />
        </div>

        <button type="submit" className="btn btn-primary">
          Crear Reserva
        </button>
      </form>
    </div>
  );
};

export default ReservaForm;
