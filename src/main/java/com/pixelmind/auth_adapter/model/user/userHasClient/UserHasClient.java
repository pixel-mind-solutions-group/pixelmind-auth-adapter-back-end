//package com.pixelmind.auth_adapter.model.user.userHasClient;
//
//import com.pixelmind.auth_adapter.model.AuditData;
//import com.pixelmind.auth_adapter.model.client.Client;
//import com.pixelmind.auth_adapter.model.user.User;
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
//@NoArgsConstructor
//@AllArgsConstructor
//@Entity
//public class UserHasClient {
//    @Id
//    @GeneratedValue(generator = "UUID")
//    @GenericGenerator(
//        name = "UUID",
//        strategy = "org.hibernate.id.UUIDGenerator"
//    )
//    @Column(updatable = false, nullable = false)
//    private UUID id;
//
//    @ManyToOne
//    @JoinColumn(name = "user_id")
//    private User user;
//
//    @ManyToOne
//    @JoinColumn(name = "client_id")
//    private Client client;
//
//    @Embedded
//    @AttributeOverrides(value = {
//            @AttributeOverride(name = "createdBy", column = @Column(name = "created_by")),
//            @AttributeOverride(name = "createdOn", column = @Column(name = "created_on"))
//    })
//    private AuditData auditData;
//}
