public class InventoryItem {
    private final SimpleStringProperty id = new SimpleStringProperty("");
    private final SimpleDoubleProperty price = new SimpleDoubleProperty(0.0);
    private final SimpleIntegerProperty stock = new SimpleIntegerProperty(0);

    public InventoryItem(String id, double price, int stock) {
        setId(id);
        setPrice(price);
        setStock(stock);
    }

    // Getters and setters
}

public class InventoryDAO {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/inventory";
    private static final String USER = "root";
    private static final String PASS = "";

    public ObservableList<InventoryItem> getItems() throws SQLException {
        ObservableList<InventoryItem> items = FXCollections.observableArrayList();
        String query = "SELECT * FROM products";
        
        try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            
            while (rs.next()) {
                items.add(new InventoryItem(
                    rs.getString("product_id"),
                    rs.getDouble("price"),
                    rs.getInt("stock")
                ));
            }
        }
        return items;
    }
}

public class MainApp extends Application {
    private TableView<InventoryItem> table = new TableView<>();
    
    @Override
    public void start(Stage primaryStage) {
        TableColumn<InventoryItem, String> idColumn = new TableColumn<>("Product ID");
        idColumn.setCellValueFactory(new PropertyValueFactory<>("id"));
        
        TableColumn<InventoryItem, Number> priceColumn = new TableColumn<>("Price");
        priceColumn.setCellValueFactory(new PropertyValueFactory<>("price"));
        
        TableColumn<InventoryItem, Number> stockColumn = new TableColumn<>("Stock");
        stockColumn.setCellValueFactory(new PropertyValueFactory<>("stock"));
        
        table.getColumns().addAll(idColumn, priceColumn, stockColumn);
        
        VBox vbox = new VBox(table);
        Scene scene = new Scene(vbox, 600, 400);
        
        primaryStage.setTitle("Inventory Management");
        primaryStage.setScene(scene);
        primaryStage.show();
        
        loadData();
    }
    
    private void loadData() {
        try {
            table.setItems(new InventoryDAO().getItems());
        } catch (SQLException e) {
            showErrorDialog("Database Error", e.getMessage());
        }
    }
}
