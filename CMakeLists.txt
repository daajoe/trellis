cmake_minimum_required(VERSION 3.2)

project(trellis)

set(CPACK_GENERATOR "STGZ;TGZ;TZ;ZIP")
set(CPACK_SOURCE_GENERATOR "STGZ;TGZ;TZ;ZIP")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "TREewidth LocaL Improvement Solver")
set(CPACK_PACKAGE_VENDOR "Johannes K. Fichte (lastname@dbai.tuwien.ac.at)")
set(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/README.md")
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_PACKAGE_VERSION_MAJOR "2")
set(CPACK_PACKAGE_VERSION_MINOR "0")
set(CPACK_PACKAGE_VERSION_PATCH "0")

include(CPack)
include(CTest)
include(CheckIncludeFileCXX)
include(WriteCompilerDetectionHeader)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING
            "Please choose the type of build. Options are: None Debug Release RelWithDebInfo MinSizeRel."
            FORCE )
endif()

#if (NOT DEFINED BUILD_SHARED_LIBS)
#    set(BUILD_SHARED_LIBS ON)
#endif()

if (DEFINED TRELLIS_DEBUG_OUTPUT)
    if (TRELLIS_DEBUG_OUTPUT)
        message("Debugging output is enabled!")

        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DTRELLIS_DEBUG_OUTPUT" )
    endif()
endif()

if (NOT DEFINED BUILD_TESTING)
    message("Tests are disabled!")

    set(BUILD_TESTING OFF)
endif()


#EXTERNAL DEPENDENCIES TO GIT SUBMODULES
include(ExternalProject)

set(ExternalProjectCMakeArgs
        -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}:PATH
        -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
        -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
        )

ExternalProject_Add(htd-build
        DOWNLOAD_COMMAND git submodule update
        DOWNLOAD_DIR ${PROJECT_SOURCE_DIR}
        SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/htd
        BINARY_DIR ${PROJECT_BINARY_DIR}/decomposer/htd
        STAMP_DIR ${PROJECT_BINARY_DIR}/decomposer/htd
        TMP_DIR ${PROJECT_BINARY_DIR}/decomposer/htd
        INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/htd
        PREFIX ${PROJECT_BINARY_DIR}/libs/
        INSTALL_COMMAND cmake -E copy_directory ${PROJECT_SOURCE_DIR}/decomposer/htd/bin/ ${PROJECT_SOURCE_DIR}/decomposer/htd/lib/ ${PROJECT_BINARY_DIR}/libs/htd
        )

ExternalProject_Add_Step(htd-build htd-build_sh
	COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/htd.sh ${PROJECT_SOURCE_DIR}/libs/htd/htd
	DEPENDEES install
	WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/libs/
	LOG 1
)


ExternalProject_Add(tcs-build
        DOWNLOAD_COMMAND git submodule update
        DOWNLOAD_DIR ${PROJECT_SOURCE_DIR}
        SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/tcs-meijin
        BINARY_DIR ${PROJECT_BINARY_DIR}/decomposer/tcs-meijin
        STAMP_DIR ${PROJECT_BINARY_DIR}/decomposer/tcs-meijin
        TMP_DIR ${PROJECT_BINARY_DIR}/decomposer/tcs-meijin
        INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/tcs
        CONFIGURE_COMMAND "${configure}"
        BUILD_COMMAND ${make}
        INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/tcs-meijin/tw-exact ${PROJECT_BINARY_DIR}/libs/tcs/tcs-meijin
        )

ExternalProject_Add(jdrasil-build
        DOWNLOAD_COMMAND git submodule update
        DOWNLOAD_DIR ${PROJECT_SOURCE_DIR}
        SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/Jdrasil
        BINARY_DIR ${PROJECT_BINARY_DIR}/decomposer/Jdrasil
        STAMP_DIR ${PROJECT_BINARY_DIR}/decomposer/Jdrasil
        TMP_DIR ${PROJECT_BINARY_DIR}/decomposer/Jdrasil
        CONFIGURE_COMMAND "${configure}"
        BUILD_COMMAND ${make}
        INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/jdrasil
        INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/jdrasil.sh ${PROJECT_BINARY_DIR}/libs/jdrasil/jdrasil
        )

ExternalProject_Add(bztreewidth-build
        DOWNLOAD_COMMAND git submodule update
        DOWNLOAD_DIR ${PROJECT_SOURCE_DIR}
        SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/BZTreewidth
        BINARY_DIR ${PROJECT_BINARY_DIR}/decomposer/BZTreewidth
        STAMP_DIR ${PROJECT_BINARY_DIR}/decomposer/BZTreewidth
        TMP_DIR ${PROJECT_BINARY_DIR}/decomposer/BZTreewidth
        CONFIGURE_COMMAND "${configure}"
        BUILD_COMMAND ${make}
        INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/bztw
        INSTALL_COMMAND cmake -E copy_directory ${PROJECT_SOURCE_DIR}/decomposer/BZTreewidth/bin/ ${PROJECT_BINARY_DIR}/libs/bztw
        )

ExternalProject_Add(flowcutter-build
        DOWNLOAD_COMMAND git submodule update
        DOWNLOAD_DIR ${PROJECT_SOURCE_DIR}
        SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/flow-cutter-pace16
        BINARY_DIR ${PROJECT_BINARY_DIR}/decomposer/flow-cutter-pace16
        STAMP_DIR ${PROJECT_BINARY_DIR}/decomposer/flow-cutter-pace16
        TMP_DIR ${PROJECT_BINARY_DIR}/decomposer/flow-cutter-pace16
        CONFIGURE_COMMAND "${configure}"
        BUILD_COMMAND ${make}
        INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/flc
        INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/flow-cutter-pace16//flow_cutter_pace16 ${PROJECT_BINARY_DIR}/libs/flc/flow_cutter
        )

#subdirs(src/)

#configure_file(
#        "${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
#        "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
#        IMMEDIATE @ONLY)

#find_package(Doxygen)
#if(DOXYGEN_FOUND)
#    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/Doxyfile.in ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY)
#    add_custom_target(doc
#            ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
#            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
#            COMMENT "Generate API documentation" VERBATIM
#            )
#endif(DOXYGEN_FOUND)

add_custom_target(uninstall COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)
