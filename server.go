package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	_ "github.com/lib/pq" 
)


type FaceData struct {
	Path    string `json:"path"`
	Age     int    `json:"age"`
	Gender  string `json:"gender"`
	Emotion string `json:"emotion"`
}


var validFields = map[string]string{
	"age":     "int",
	"gender":  "string",
	"emotion": "string",
}

func main() {
	
	http.Handle("/", http.FileServer(http.Dir("./")))
	http.Handle("/fotos/", http.StripPrefix("/fotos/", http.FileServer(http.Dir("./uploads"))))

	
	http.HandleFunc("/buscar", handleSearch)

	fmt.Println("🌍 Servidor Go corriendo en http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}

func handleSearch(w http.ResponseWriter, r *http.Request) {
	
	w.Header().Set("Access-Control-Allow-Origin", "*")

	query := strings.ToLower(r.URL.Query().Get("q"))

	
	if !strings.HasPrefix(query, "find faces where") {
		http.Error(w, "Error sintáctico: Debe empezar con 'FIND faces WHERE'", http.StatusBadRequest)
		return
	}

	conditionPart := strings.TrimPrefix(query, "find faces where ")
	parts := strings.Fields(conditionPart) 

	if len(parts) < 1 {
		http.Error(w, "Consulta incompleta", http.StatusBadRequest)
		return
	}

	
	fieldName := parts[0]
	if _, ok := validFields[fieldName]; !ok {
		msg := fmt.Sprintf("Error semántico: campo '%s' no permitido. Válidos: age, gender, emotion", fieldName)
		http.Error(w, msg, http.StatusBadRequest)
		return
	}

	

	db, err := sql.Open("postgres", "user=postgres password=102538 dbname=face_attributes sslmode=disable")
	if err != nil {
		http.Error(w, "Error de conexión a DB", 500)
		return
	}
	defer db.Close()

	sqlQuery := "SELECT image_path, age, gender, emotion FROM face_attributes WHERE " + conditionPart

	rows, err := db.Query(sqlQuery)
	if err != nil {
		http.Error(w, "Error al ejecutar consulta: "+err.Error(), 500)
		return
	}
	defer rows.Close()

	resultados := []FaceData{}
	for rows.Next() {
		var f FaceData
		var fullPath string
		rows.Scan(&fullPath, &f.Age, &f.Gender, &f.Emotion)

		
		fileName := strings.Split(fullPath, "uploads")[1]
		f.Path = "/fotos" + strings.ReplaceAll(fileName, "\\", "/")

		resultados = append(resultados, f)
	}

	
	json.NewEncoder(w).Encode(resultados)
}
