package com.droneshield.cloudapp.controller;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import jdk.internal.org.jline.utils.Log;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Controller
public class BaseController {
    
    @GetMapping("/")
    public String indexPage() {
      
        return "index";
    }
}
