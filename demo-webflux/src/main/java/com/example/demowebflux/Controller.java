package com.example.demowebflux;

import com.fasterxml.jackson.databind.JsonNode;
import com.vladmihalcea.hibernate.type.json.JsonNodeBinaryType;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import javax.persistence.EntityManager;
import java.util.List;
import java.util.Objects;

@CrossOrigin
@Log4j2
@RestController
@RequestMapping("/api")
public class Controller {
  @Autowired private EntityManager entityManager;

  @GetMapping("/thing/{id}")
  public Mono<ResponseEntity<JsonNode>> get(@PathVariable Integer id, ServerHttpResponse response) {
    return getById(id)
        .filter(Objects::nonNull)
        .map(r -> new ResponseEntity<>(r, HttpStatus.OK))
        .switchIfEmpty(Mono.defer(() -> Mono.just(new ResponseEntity<>(HttpStatus.NOT_FOUND))));
  }

  private Mono<JsonNode> getById(Integer id) {
    log.info(String.format(">>>> gettingById(%s)", id));
    List myJson =
        entityManager
            .createNativeQuery("SELECT my_json FROM my_json_table WHERE id = :id")
            .setParameter("id", id)
            .unwrap(org.hibernate.query.NativeQuery.class)
            .addScalar("my_json", JsonNodeBinaryType.INSTANCE)
            .getResultList();

    if (myJson.isEmpty()) {
      return Mono.empty();
    } else {
      return Mono.just((JsonNode) myJson.get(0));
    }
  }
}
