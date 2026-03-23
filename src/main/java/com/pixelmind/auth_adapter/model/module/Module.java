//package com.pixelmind.auth_adapter.model.module;
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
//import java.util.UUID;
//
//@Getter
//@Setter
//@Entity
//@NoArgsConstructor
//@AllArgsConstructor
//@Table
//public class Module {
//    @Id
//    @GeneratedValue(generator = "UUID")
//    @GenericGenerator(
//        name = "UUID",
//        strategy = "org.hibernate.id.UUIDGenerator"
//    )
//    @Column(updatable = false, nullable = false)
//    private UUID id;
//    private String name;
//    private String description;
//
//    @ManyToOne
//    @JoinColumn(name = "client_id")
//    private Client client;
//}
