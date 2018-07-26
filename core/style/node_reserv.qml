<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.2.1-Bonn" minScale="1e+8" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyDrawingHints="0" readOnly="0" labelsEnabled="0" simplifyAlgorithm="0" maxScale="0" simplifyDrawingTol="1">
  <renderer-v2 symbollevels="0" forceraster="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol name="0" clip_to_extent="1" type="marker" alpha="1">
        <layer class="SimpleMarker" enabled="1" locked="0" pass="0">
          <prop v="0" k="angle"/>
          <prop v="0,170,255,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="square" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,255,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="area" k="scale_method"/>
          <prop v="3" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
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
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory lineSizeType="MM" penWidth="0" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" minimumSize="0" barWidth="5" scaleBasedVisibility="0" penAlpha="255" diagramOrientation="Up" width="15" sizeType="MM" opacity="1" height="15" maxScaleDenominator="1e+8" scaleDependency="Area" penColor="#000000" labelPlacementMethod="XHeight" enabled="0" rotationOffset="270" minScaleDenominator="0" backgroundAlpha="255" sizeScale="3x:0,0,0,0,0,0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" placement="0" zIndex="0" priority="0" dist="0" obstacle="0">
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
    <field name="HEAD">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PATTERN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_DEM">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RESULT_PRE">
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
    <alias name="" field="HEAD" index="1"/>
    <alias name="" field="PATTERN" index="2"/>
    <alias name="" field="RESULT_DEM" index="3"/>
    <alias name="" field="RESULT_PRE" index="4"/>
    <alias name="" field="RESULT_HEA" index="5"/>
    <alias name="" field="RESULT_QUA" index="6"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" field="DC_ID" applyOnUpdate="0"/>
    <default expression="" field="HEAD" applyOnUpdate="0"/>
    <default expression="" field="PATTERN" applyOnUpdate="0"/>
    <default expression="" field="RESULT_DEM" applyOnUpdate="0"/>
    <default expression="" field="RESULT_PRE" applyOnUpdate="0"/>
    <default expression="" field="RESULT_HEA" applyOnUpdate="0"/>
    <default expression="" field="RESULT_QUA" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" notnull_strength="0" field="DC_ID" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="HEAD" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="PATTERN" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="RESULT_DEM" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="RESULT_PRE" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="RESULT_HEA" constraints="0" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" field="RESULT_QUA" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="DC_ID" exp="" desc=""/>
    <constraint field="HEAD" exp="" desc=""/>
    <constraint field="PATTERN" exp="" desc=""/>
    <constraint field="RESULT_DEM" exp="" desc=""/>
    <constraint field="RESULT_PRE" exp="" desc=""/>
    <constraint field="RESULT_HEA" exp="" desc=""/>
    <constraint field="RESULT_QUA" exp="" desc=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="DC_ID" type="field" width="-1" hidden="0"/>
      <column name="HEAD" type="field" width="-1" hidden="0"/>
      <column name="PATTERN" type="field" width="-1" hidden="0"/>
      <column name="RESULT_DEM" type="field" width="-1" hidden="0"/>
      <column name="RESULT_PRE" type="field" width="-1" hidden="0"/>
      <column name="RESULT_HEA" type="field" width="-1" hidden="0"/>
      <column name="RESULT_QUA" type="field" width="-1" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <editform>C:/Users/Ana/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QWater/samples/d-w/lps</editform>
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
    <field name="HEAD" editable="1"/>
    <field name="PATTERN" editable="1"/>
    <field name="RESULT_DEM" editable="1"/>
    <field name="RESULT_HEA" editable="1"/>
    <field name="RESULT_PRE" editable="1"/>
    <field name="RESULT_QUA" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="DC_ID" labelOnTop="0"/>
    <field name="HEAD" labelOnTop="0"/>
    <field name="PATTERN" labelOnTop="0"/>
    <field name="RESULT_DEM" labelOnTop="0"/>
    <field name="RESULT_HEA" labelOnTop="0"/>
    <field name="RESULT_PRE" labelOnTop="0"/>
    <field name="RESULT_QUA" labelOnTop="0"/>
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
