<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" labelsEnabled="0" simplifyAlgorithm="0" simplifyLocal="1" hasScaleBasedVisibilityFlag="0" minScale="1e+8" maxScale="0" simplifyDrawingHints="0" simplifyMaxScale="1" version="3.0.1-Girona" simplifyDrawingTol="1">
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" clip_to_extent="1" type="marker" alpha="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
          <prop k="angle" v="90"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="triangle"/>
          <prop k="offset" v="0,-0.5"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="3"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory penWidth="0" lineSizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" width="15" sizeType="MM" height="15" minimumSize="0" labelPlacementMethod="XHeight" penColor="#000000" opacity="1" enabled="0" backgroundAlpha="255" diagramOrientation="Up" sizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" maxScaleDenominator="1e+8" scaleBasedVisibility="0" barWidth="5" penAlpha="255" rotationOffset="270" minScaleDenominator="0" scaleDependency="Area">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" linePlacementFlags="18" dist="0" showAll="1" placement="0" zIndex="0" priority="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="DC_ID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ELEVATION">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PROPERTIES">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_REA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_FRI">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_HEA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_STA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_FLO">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_VEL">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_QUA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="DC_ID" index="0"/>
    <alias name="" field="ELEVATION" index="1"/>
    <alias name="" field="PROPERTIES" index="2"/>
    <alias name="" field="RESULT_REA" index="3"/>
    <alias name="" field="RESULT_FRI" index="4"/>
    <alias name="" field="RESULT_HEA" index="5"/>
    <alias name="" field="RESULT_STA" index="6"/>
    <alias name="" field="RESULT_FLO" index="7"/>
    <alias name="" field="RESULT_VEL" index="8"/>
    <alias name="" field="RESULT_QUA" index="9"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="DC_ID" expression=""/>
    <default applyOnUpdate="0" field="ELEVATION" expression=""/>
    <default applyOnUpdate="0" field="PROPERTIES" expression=""/>
    <default applyOnUpdate="0" field="RESULT_REA" expression=""/>
    <default applyOnUpdate="0" field="RESULT_FRI" expression=""/>
    <default applyOnUpdate="0" field="RESULT_HEA" expression=""/>
    <default applyOnUpdate="0" field="RESULT_STA" expression=""/>
    <default applyOnUpdate="0" field="RESULT_FLO" expression=""/>
    <default applyOnUpdate="0" field="RESULT_VEL" expression=""/>
    <default applyOnUpdate="0" field="RESULT_QUA" expression=""/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="DC_ID" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="ELEVATION" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="PROPERTIES" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="RESULT_REA" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="RESULT_FRI" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="RESULT_HEA" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="RESULT_STA" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="RESULT_FLO" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="RESULT_VEL" notnull_strength="0"/>
    <constraint exp_strength="0" unique_strength="0" constraints="0" field="RESULT_QUA" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="DC_ID" desc=""/>
    <constraint exp="" field="ELEVATION" desc=""/>
    <constraint exp="" field="PROPERTIES" desc=""/>
    <constraint exp="" field="RESULT_REA" desc=""/>
    <constraint exp="" field="RESULT_FRI" desc=""/>
    <constraint exp="" field="RESULT_HEA" desc=""/>
    <constraint exp="" field="RESULT_STA" desc=""/>
    <constraint exp="" field="RESULT_FLO" desc=""/>
    <constraint exp="" field="RESULT_VEL" desc=""/>
    <constraint exp="" field="RESULT_QUA" desc=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column name="DC_ID" type="field" hidden="0" width="-1"/>
      <column name="ELEVATION" type="field" hidden="0" width="-1"/>
      <column name="PROPERTIES" type="field" hidden="0" width="-1"/>
      <column name="RESULT_REA" type="field" hidden="0" width="-1"/>
      <column name="RESULT_FRI" type="field" hidden="0" width="-1"/>
      <column name="RESULT_HEA" type="field" hidden="0" width="-1"/>
      <column name="RESULT_STA" type="field" hidden="0" width="-1"/>
      <column name="RESULT_FLO" type="field" hidden="0" width="-1"/>
      <column name="RESULT_VEL" type="field" hidden="0" width="-1"/>
      <column name="RESULT_QUA" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <editform>C:/Users/jorgealmerio/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QWater_q3/samples/d-w/lps</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="DC_ID" editable="1"/>
    <field name="ELEVATION" editable="1"/>
    <field name="PROPERTIES" editable="1"/>
    <field name="RESULT_FLO" editable="1"/>
    <field name="RESULT_FRI" editable="1"/>
    <field name="RESULT_HEA" editable="1"/>
    <field name="RESULT_QUA" editable="1"/>
    <field name="RESULT_REA" editable="1"/>
    <field name="RESULT_STA" editable="1"/>
    <field name="RESULT_VEL" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="DC_ID" labelOnTop="0"/>
    <field name="ELEVATION" labelOnTop="0"/>
    <field name="PROPERTIES" labelOnTop="0"/>
    <field name="RESULT_FLO" labelOnTop="0"/>
    <field name="RESULT_FRI" labelOnTop="0"/>
    <field name="RESULT_HEA" labelOnTop="0"/>
    <field name="RESULT_QUA" labelOnTop="0"/>
    <field name="RESULT_REA" labelOnTop="0"/>
    <field name="RESULT_STA" labelOnTop="0"/>
    <field name="RESULT_VEL" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>DC_ID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
