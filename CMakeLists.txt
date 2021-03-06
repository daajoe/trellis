cmake_minimum_required(VERSION 3.5)

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


#TODO: error message
#if(UNIX AND NOT APPLE)
#    # for Linux, BSD, Solaris, Minix
#endif()

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


#BUGFIXED CMAKE MODULE FOR GIT STASH OF UNTRACKED FILES
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules/")
#EXTERNAL DEPENDENCIES TO GIT SUBMODULES
include(ExternalProject)

set(ExternalProjectCMakeArgs
  -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}:PATH
  -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
  -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
  -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  )

ExternalProject_Add(htd2016
  GIT_REPOSITORY https://github.com/mabseher/htd.git
  #PACE 2016 VERSION
  #GIT_TAG 4587fba
  #PREPACE 2017 VERSION including bugfixes and additional options
  GIT_TAG 075019f
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/htd
  BUILD_IN_SOURCE 1
  PREFIX build/htd2016
  #PREFIX ${PROJECT_BINARY_DIR}/libs/
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/htd2016
  INSTALL_COMMAND cmake -E copy_directory ${PROJECT_SOURCE_DIR}/decomposer/pace2016/htd/bin/ ${PROJECT_SOURCE_DIR}/decomposer/pace2016/htd/lib/ ${PROJECT_BINARY_DIR}/libs/htd2016
  )

ExternalProject_Add_Step(htd2016 htd2016_sh
  COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/htd2016.sh ${PROJECT_SOURCE_DIR}/libs/htd2016/htd
  DEPENDEES install
  WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/libs/
  LOG 1
)


ExternalProject_Add(htd2017
  GIT_REPOSITORY https://github.com/mabseher/htd.git
  GIT_TAG 6236c0a
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/latest/htd
  BUILD_IN_SOURCE 1
  PREFIX build/htd2017
  #PREFIX ${PROJECT_BINARY_DIR}/libs/
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/htd2017
  INSTALL_COMMAND cmake -E copy_directory ${PROJECT_SOURCE_DIR}/decomposer/latest/htd/bin/ ${PROJECT_SOURCE_DIR}/decomposer/pace2016/htd/lib/ ${PROJECT_BINARY_DIR}/libs/htd2017
  )

ExternalProject_Add_Step(htd2017 htd2017_sh
  COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/htd2017.sh ${PROJECT_SOURCE_DIR}/libs/htd2017/htd
  DEPENDEES install
  WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/libs/
  LOG 1
)


ExternalProject_Add(tamaki2016
  GIT_REPOSITORY https://github.com/daajoe/treewidth-exact
  #Bugfix: original repository
  #https://github.com/TCS-Meiji/treewidth-exact.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/tamaki
  BUILD_IN_SOURCE 1
  PREFIX build/tamaki2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/tamaki2016
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/pace2016/tamaki/tw-exact ${PROJECT_BINARY_DIR}/libs/tamaki2016/tamaki
  )

ExternalProject_Add(tamaki2017
  GIT_REPOSITORY https://github.com/daajoe/PACE2017-TrackA.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/latest/tamaki
  BUILD_IN_SOURCE 1
  PREFIX build/tamaki2017
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/tamaki2017
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/tamaki2017-exact.sh ${PROJECT_BINARY_DIR}/libs/tamaki2017/tamaki-exact
  )

ExternalProject_Add_Step(tamaki2017 tamaki2017_sh
  COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/tamaki2017-heuristic.sh ${PROJECT_BINARY_DIR}/libs/tamaki2017/tamaki-heuristic
  DEPENDEES install
  WORKING_DIRECTORY ${PROJECT_BINARY_DIR}/libs/
  LOG 1
  )

      
ExternalProject_Add(jdrasil2016
  GIT_REPOSITORY https://github.com/daajoe/Jdrasil.git
  GIT_TAG origin/sat_runtmlm
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/Jdrasil
  BUILD_IN_SOURCE 1
  PREFIX build/jdrasil2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/jdrasil2016
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/jdrasil2016.sh ${PROJECT_BINARY_DIR}/libs/jdrasil2016/jdrasil
  )


ExternalProject_Add(jdrasil2017
  GIT_REPOSITORY https://github.com/daajoe/Jdrasil.git
  #GIT_TAG 0240973
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/latest/Jdrasil
  BUILD_IN_SOURCE 1
  PREFIX build/jdrasil2017
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND gradle pace
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/jdrasil2017
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/jdrasil2017.sh ${PROJECT_BINARY_DIR}/libs/jdrasil2017/jdrasil
  )

ExternalProject_Add(bztreewidth2016
  GIT_REPOSITORY https://github.com/TomvdZanden/BZTreewidth.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/BZTreewidth
  BUILD_IN_SOURCE 1
  PREFIX build/bztreewidth2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/bztreewidth2016
  INSTALL_COMMAND cmake -E copy_directory ${PROJECT_SOURCE_DIR}/decomposer/pace2016/BZTreewidth/bin/ ${PROJECT_BINARY_DIR}/libs/bztreewidth2016
  )

ExternalProject_Add(flowcutter2016
  GIT_REPOSITORY https://github.com/ben-strasser/flow-cutter-pace16.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/flow-cutter-pace16
  BUILD_IN_SOURCE 1
  PREFIX build/flowcutter2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/flowcutter2016
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/pace2016/flow-cutter-pace16/flow_cutter_pace16 ${PROJECT_BINARY_DIR}/libs/flowcutter2016/flowcutter
  )

ExternalProject_Add(flowcutter2017
  GIT_REPOSITORY https://github.com/kit-algo/flow-cutter-pace17.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/latest/Flow-Cutter
  BUILD_IN_SOURCE 1
  PREFIX build/flowcutter2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/flowcutter2017
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/latest/Flow-Cutter/flow_cutter_pace17 ${PROJECT_BINARY_DIR}/libs/flowcutter2017/flowcutter
  )


ExternalProject_Add(tdvalidate
  GIT_REPOSITORY https://github.com/daajoe/td-validate.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/td-validate
  BUILD_IN_SOURCE 1
  PREFIX build/tdvalidate
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/tdvalidate
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/td-validate/td-validate ${PROJECT_BINARY_DIR}/libs/tdvalidate/tdvalidate
  )


ExternalProject_Add(tdlib2017
  GIT_REPOSITORY https://github.com/freetdi/p17.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/latest/tdlib
  BUILD_IN_SOURCE 1
  PREFIX build/tdlib2017
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/tdlib2017
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/latest/tdlib/build/grtd/grtd ${PROJECT_BINARY_DIR}/libs/tdlib2017/tdlib
  )


ExternalProject_Add(minfill_mrs2017
  GIT_REPOSITORY https://github.com/td-mrs/minfill_mrs.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/latest/minfill_mrs
  BUILD_IN_SOURCE 1
  PREFIX build/minfill_mrs2017
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/minfillmrs2017
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/latest/minfill_mrs/minfill_mrs ${PROJECT_BINARY_DIR}/libs/minfillmrs2017/minfillmrs
  )


ExternalProject_Add(minfillbg_mrs2017
  GIT_REPOSITORY https://github.com/td-mrs/minfillbg_mrs.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/latest/minfillbg_mrs
  BUILD_IN_SOURCE 1
  PREFIX build/minfillbg_mrs2017
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/minfillbgmrs2017
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/latest/minfillbg_mrs/minfillbg_mrs ${PROJECT_BINARY_DIR}/libs/minfillmrs2017/minfillbgmrs
  )


ExternalProject_Add(mfjones2016
  GIT_REPOSITORY https://github.com/mfjones/pace2016.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/mfjones
  BUILD_IN_SOURCE 1
  PREFIX build/mfjones2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/mfjones2016
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/wrappers/mfjones.sh  ${PROJECT_BINARY_DIR}/libs/mfjones2016/mfjones
  )

ExternalProject_Add(mrprajesh2016
  GIT_REPOSITORY https://github.com/mrprajesh/pacechallenge.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/mrprajesh
  BUILD_IN_SOURCE 1
  PREFIX build/mrprajesh2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/mrprajesh2016
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/pace2016/mrprajesh/tw-heuristic ${PROJECT_BINARY_DIR}/libs/mrprajesh2016/mrprajesh
  )


ExternalProject_Add(elithelli2016
  GIT_REPOSITORY https://github.com/elitheeli/2016-pace-challenge.git
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/decomposer/pace2016/elithelli
  BUILD_IN_SOURCE 1
  PREFIX build/mrprajesh2016
  CONFIGURE_COMMAND "${configure}"
  BUILD_COMMAND ${make}
  INSTALL_DIR ${PROJECT_BINARY_DIR}/libs/elithelli2016
  INSTALL_COMMAND cmake -E copy ${PROJECT_SOURCE_DIR}/decomposer/pace2016/elithelli/tw-heuristic ${PROJECT_BINARY_DIR}/libs/elithelli2016/elithelli
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
