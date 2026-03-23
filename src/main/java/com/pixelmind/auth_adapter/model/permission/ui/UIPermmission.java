//package com.pixelmind.auth_adapter.model.permission.ui;
//
//import com.pixelmind.auth_adapter.model.client.Client;
//import jakarta.persistence.*;
//import lombok.AllArgsConstructor;
//import lombok.Getter;
//import lombok.NoArgsConstructor;
//import lombok.Setter;
//import org.hibernate.annotations.GenericGenerator;
//import org.hibernate.annotations.UuidGenerator;
//
//@Getter
//@Setter
//@Entity
//@NoArgsConstructor
//@AllArgsConstructor
//@Table
//public class UIPermmission {
//    @Id
//    @GeneratedValue(generator = "UUID")
//    @GenericGenerator(
//        name = "UUID",
//        strategy = "org.hibernate.id.UUIDGenerator"
//    )
//    @Column(updatable = false, nullable = false)
//    private Integer id;
//    private String name;
//    private String description;
//
//    @ManyToOne
//    @JoinColumn(name = "client_id")
//    private Client client;
//}
