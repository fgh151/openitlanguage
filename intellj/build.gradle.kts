plugins {
    id("java")
    id("org.jetbrains.kotlin.jvm") version "1.9.20"
    id("org.jetbrains.intellij") version "1.16.1"
    id("org.jetbrains.grammarkit") version "2022.3.2.1"
}

group = "ru.openitstudio.language"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

sourceSets {
    main {
        java {
            srcDirs("src/main/gen")
        }
    }
}

// Configure Gradle IntelliJ Plugin
intellij {
    version.set("2023.1.5")
    type.set("IC") // Target IDE Platform

    plugins.set(listOf(/* Plugin Dependencies */))
}

tasks {
    // Set the JVM compatibility versions
    withType<JavaCompile> {
        sourceCompatibility = "17"
        targetCompatibility = "17"
    }
    withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
        kotlinOptions.jvmTarget = "17"
    }

    patchPluginXml {
        sinceBuild.set("231")
        untilBuild.set("243.*")
    }

    signPlugin {
        certificateChain.set(System.getenv("CERTIFICATE_CHAIN"))
        privateKey.set(System.getenv("PRIVATE_KEY"))
        password.set(System.getenv("PRIVATE_KEY_PASSWORD"))
    }

    publishPlugin {
        token.set(System.getenv("PUBLISH_TOKEN"))
    }

    generateLexer {
        sourceFile.set(file("src/main/grammar/Opnit.flex"))
        targetDir.set("src/main/gen/ru/openitstudio/language/lexer")
        targetClass.set("_OpnitLexer")
        purgeOldFiles.set(true)
    }

    generateParser {
        sourceFile.set(file("src/main/grammar/Opnit.bnf"))
        targetRoot.set("src/main/gen")
        pathToParser.set("/ru/openitstudio/language/parser/OpnitParser.java")
        pathToPsiRoot.set("/ru/openitstudio/language/psi")
        purgeOldFiles.set(true)
    }

    compileKotlin {
        dependsOn(generateLexer, generateParser)
    }
} 