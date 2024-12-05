import { useState, useEffect } from "react";
import apiClient from "../api/client";
import "../style.css";  

const Reservas = () => {
  const [reservas, setReservas] = useState<any[]>([]);
  const [dia, setDia] = useState("");
  const [canchaId, setCanchaId] = useState("");
  const [, setLoading] = useState(false);
  const [editingReserva, setEditingReserva] = useState<any | null>(null);
  const [editForm, setEditForm] = useState({
    hora: "",
    duracion: 0,
  });

  const fetchReservas = async () => {
    if (!dia || !canchaId) return;
    setLoading(true);
    try {
      const response = await apiClient.get("/api/reservas", {
        params: { dia, cancha_id: canchaId },
      });
      setReservas(response.data);
    } catch (error) {
      console.error(error);
      alert("Error al obtener reservas. Intente de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const eliminarReserva = async (id: number) => {
    if (!window.confirm("¿Seguro que deseas eliminar esta reserva?")) return;

    try {
      await apiClient.delete(`/api/reservas/${id}`);
      alert("Reserva eliminada con éxito.");
      setReservas(reservas.filter((reserva) => reserva.id !== id));
    } catch (error) {
      console.error(error);
      alert("Error al eliminar la reserva.");
    }
  };

  const iniciarEdicion = (reserva: any) => {
    setEditingReserva(reserva);
    setEditForm({
      hora: reserva.hora,
      duracion: reserva.duracion,
    });
  };

  const cancelarEdicion = () => {
    setEditingReserva(null);
    setEditForm({
      hora: "",
      duracion: 0,
    });
  };

  const guardarEdicion = async () => {
    if (!editingReserva) return;

    try {
      await apiClient.put(`/api/reservas/${editingReserva.id}`, {
        ...editForm,
        dia,
        cancha_id: canchaId,
      });
      alert("Reserva actualizada con éxito.");
      setEditingReserva(null);
      fetchReservas();
    } catch (error) {
      console.error(error);
      alert("Error al actualizar la reserva.");
    }
  };

  useEffect(() => {
    if (dia && canchaId) {
      fetchReservas();
    }
  }, [dia, canchaId]);

  const formatHora = (hora: string) => {
    const [hours, minutes] = hora.split(":");
    return `${hours}:${minutes}`;
  };

  return (
    <div className="container">
      <h2>Consultar Reservas</h2>

      <div className="form-group">
        <label htmlFor="dia">Fecha</label>
        <input
          type="date"
          value={dia}
          onChange={(e) => setDia(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="canchaId">Seleccionar Cancha</label>
        <select
          value={canchaId}
          onChange={(e) => setCanchaId(e.target.value)}
        >
          <option value="">Seleccionar cancha</option>
          <option value="1">Cancha 1</option>
          <option value="2">Cancha 2</option>
        </select>
      </div>


      {reservas.length === 0 && <p>No hay reservas para esta fecha y cancha.</p>}

      <ul>
        {reservas.map((reserva: any) => (
          <li key={reserva.id}>
            {reserva.nombre_contacto} - {formatHora(reserva.hora)} ({reserva.duracion} mins)
            <div>
              <button
                onClick={() => eliminarReserva(reserva.id)}
                className="btn btn-danger"
              >
                Eliminar
              </button>
              <button
                onClick={() => iniciarEdicion(reserva)}
                className="btn btn-primary"
              >
                Editar
              </button>
            </div>
          </li>
        ))}
      </ul>

      {editingReserva && (
        <div className="edit-form">
          <h3>Editar Reserva</h3>
          <div className="form-group">
            <label>Hora</label>
            <input
              type="time"
              value={editForm.hora}
              onChange={(e) =>
                setEditForm({ ...editForm, hora: e.target.value })
              }
            />
          </div>

          <div className="form-group">
            <label>Duración (minutos)</label>
            <input
              type="number"
              value={editForm.duracion}
              onChange={(e) =>
                setEditForm({ ...editForm, duracion: parseInt(e.target.value) })
              }
            />
          </div>

          <div>
            <button onClick={guardarEdicion} className="btn btn-success">
              Guardar
            </button>
            <button onClick={cancelarEdicion} className="btn btn-secondary">
              Cancelar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reservas;
