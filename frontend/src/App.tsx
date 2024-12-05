import { useState } from "react";
import { Container, Card, Row, Col, Button } from "react-bootstrap";
import ReservaForm from "./components/ReservaForm";
import Reservas from "./pages/Reservas";
import "./style.css";  

function App() {
  const [mostrarFormulario, setMostrarFormulario] = useState(true); // Controla la vista del formulario y las reservas

  return (
    <Container className="mt-5">
      <Card className="mb-4">
        <Card.Body>
          <h1 className="text-center mb-4">Reserva de Canchas de Padel</h1>

          <Row className="mb-3">
            <Col className="text-center">
              <Button
                variant={mostrarFormulario ? "outline-primary" : "primary"}
                onClick={() => setMostrarFormulario(!mostrarFormulario)}
              >
                {mostrarFormulario ? "Ver Reservas" : "Crear Reserva"}
              </Button>
            </Col>
          </Row>

          {/* Condicional para mostrar el formulario o las reservas */}
          {mostrarFormulario ? (
            <ReservaForm />
          ) : (
            <Reservas />
          )}
        </Card.Body>
      </Card>
    </Container>
  );
}

export default App;
